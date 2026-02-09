"""
Enhanced Voice Activity Detection (VAD) module for meeting environments.
Filters out background noise and only processes actual speech.
"""

import numpy as np
from collections import deque
from typing import Optional

class EnhancedVAD:
    """
    Enhanced Voice Activity Detection optimized for meeting environments.
    Uses multiple techniques to filter background noise:
    - RMS energy threshold
    - Zero-crossing rate (speech has higher ZCR than noise)
    - Spectral centroid (speech has different frequency characteristics)
    - Adaptive noise floor estimation
    """
    
    def __init__(
        self,
        energy_threshold: float = 0.008,  # RMS threshold (tuned for meetings)
        zcr_threshold: float = 0.01,  # Zero-crossing rate threshold
        min_speech_duration: float = 0.3,  # Minimum speech duration in seconds
        noise_floor_samples: int = 10,  # Samples to use for noise floor estimation
    ):
        self.energy_threshold = energy_threshold
        self.zcr_threshold = zcr_threshold
        self.min_speech_duration = min_speech_duration
        self.noise_floor_samples = noise_floor_samples
        
        # Adaptive noise floor estimation
        self.noise_floor_history = deque(maxlen=noise_floor_samples)
        self.estimated_noise_floor = 0.002  # Initial estimate
        
        # Speech state tracking
        self.speech_start_time = None
        self.last_speech_time = None
        
    def calculate_rms_energy(self, audio: np.ndarray) -> float:
        """Calculate Root Mean Square energy of audio."""
        return np.sqrt(np.mean(audio ** 2))
    
    def calculate_zero_crossing_rate(self, audio: np.ndarray) -> float:
        """
        Calculate Zero-Crossing Rate (ZCR).
        Speech typically has higher ZCR than background noise.
        """
        if len(audio) < 2:
            return 0.0
        
        # Count zero crossings
        sign_changes = np.sum(np.diff(np.signbit(audio)))
        zcr = sign_changes / len(audio)
        return zcr
    
    def calculate_spectral_centroid(self, audio: np.ndarray, sample_rate: int) -> float:
        """
        Calculate spectral centroid - indicates where the "center of mass" of the spectrum is.
        Speech typically has spectral centroid in the 1-4 kHz range.
        """
        if len(audio) < 64:  # Need minimum samples for FFT
            return 0.0
        
        # Compute FFT
        fft = np.fft.rfft(audio)
        magnitude = np.abs(fft)
        
        # Frequency bins
        freqs = np.fft.rfftfreq(len(audio), 1.0 / sample_rate)
        
        # Avoid division by zero
        if np.sum(magnitude) == 0:
            return 0.0
        
        # Calculate weighted average frequency
        centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
        return centroid
    
    def update_noise_floor(self, audio: np.ndarray):
        """Update adaptive noise floor estimation."""
        rms = self.calculate_rms_energy(audio)
        
        # Only update if this looks like noise (low energy, low ZCR)
        zcr = self.calculate_zero_crossing_rate(audio)
        
        if rms < self.energy_threshold * 0.5 and zcr < self.zcr_threshold * 0.5:
            self.noise_floor_history.append(rms)
            if len(self.noise_floor_history) >= self.noise_floor_samples:
                self.estimated_noise_floor = np.median(list(self.noise_floor_history))
    
    def has_voice_activity(
        self,
        audio: np.ndarray,
        sample_rate: int,
        current_time: Optional[float] = None
    ) -> bool:
        """
        Determine if audio chunk contains voice activity.
        
        Returns True if the audio appears to contain speech, False otherwise.
        """
        if len(audio) == 0:
            return False
        
        # Calculate features
        rms_energy = self.calculate_rms_energy(audio)
        zcr = self.calculate_zero_crossing_rate(audio)
        spectral_centroid = self.calculate_spectral_centroid(audio, sample_rate)
        
        # Update noise floor (adaptive)
        self.update_noise_floor(audio)
        
        # Primary check: RMS energy must be above threshold
        energy_above_threshold = rms_energy > self.energy_threshold
        
        # Secondary check: Energy should be significantly above noise floor
        # (at least 2x the noise floor to avoid processing background noise)
        energy_above_noise = rms_energy > (self.estimated_noise_floor * 2.0)
        
        # Tertiary check: Zero-crossing rate (speech has characteristic ZCR)
        zcr_check = zcr > self.zcr_threshold * 0.5  # More lenient ZCR check
        
        # Spectral centroid check: Speech typically has centroid in 500-5000 Hz range
        spectral_check = 500 < spectral_centroid < 5000 if spectral_centroid > 0 else False
        
        # Decision: Require energy checks AND at least one other feature
        has_voice = (
            energy_above_threshold and
            energy_above_noise and
            (zcr_check or spectral_check)
        )
        
        # Debug output (can be disabled in production)
        if has_voice:
            print(
                f"VAD: SPEECH detected | "
                f"RMS: {rms_energy:.4f} | "
                f"ZCR: {zcr:.4f} | "
                f"Centroid: {spectral_centroid:.0f}Hz | "
                f"Noise floor: {self.estimated_noise_floor:.4f}"
            )
        else:
            print(
                f"VAD: Noise/silence | "
                f"RMS: {rms_energy:.4f} | "
                f"Threshold: {self.energy_threshold:.4f}"
            )
        
        return has_voice


# Convenience function for backward compatibility
def has_voice_activity(
    audio_chunk: np.ndarray,
    sample_rate: int = 16000,
    threshold: Optional[float] = None
) -> bool:
    """
    Simple wrapper function for backward compatibility.
    Uses enhanced VAD with default settings optimized for meetings.
    """
    vad = EnhancedVAD(
        energy_threshold=threshold if threshold is not None else 0.008
    )
    return vad.has_voice_activity(audio_chunk, sample_rate)
