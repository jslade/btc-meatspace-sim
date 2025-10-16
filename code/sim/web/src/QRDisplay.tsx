import { useEffect, useRef } from 'react';
import QRCode from 'qrcode';

interface QRDisplayProps {
  data: string;
  size?: number;
}

export function QRDisplay({ data, size = 256 }: QRDisplayProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (canvasRef.current && data) {
      QRCode.toCanvas(
        canvasRef.current,
        data,
        {
          width: size,
          margin: 2,
          color: {
            dark: '#000000',
            light: '#FFFFFF',
          },
        },
        (error) => {
          if (error) console.error('QR Code generation error:', error);
        }
      );
    }
  }, [data, size]);

  return (
    <div className="qr-display" style={{ textAlign: 'center' }}>
      <canvas ref={canvasRef} />
    </div>
  );
}
