import React from 'react';

interface GlobeLogoProps {
    className?: string;
    size?: number;
}

export const GlobeLogo: React.FC<GlobeLogoProps> = ({ className = '', size = 40 }) => {
    return (
        <img
            className={className}
            src="/globe-logo.png"
            alt="Global Talk globe logo"
            style={{
                width: size,
                height: size,
                display: 'block',
                objectFit: 'contain',
            }}
        />
    );
};
