import { useEffect, useRef, useState } from 'react';
import { Html5Qrcode } from 'html5-qrcode';

interface QRScannerProps {
  onScan: (data: string) => void;
  onError?: (error: string) => void;
}

export function QRScanner({ onScan, onError }: QRScannerProps) {
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState<string>('');
  const scannerRef = useRef<Html5Qrcode | null>(null);
  const elementId = 'qr-reader';

  const startScanning = async () => {
    try {
      setError('');
      const scanner = new Html5Qrcode(elementId);
      scannerRef.current = scanner;

      await scanner.start(
        { facingMode: 'environment' },
        {
          fps: 10,
          qrbox: { width: 250, height: 250 },
        },
        (decodedText) => {
          onScan(decodedText);
        },
        (errorMessage) => {
          // Ignore scan errors (no QR code in frame)
          console.debug('QR scan error:', errorMessage);
        }
      );

      setIsScanning(true);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to start camera';
      setError(errorMsg);
      if (onError) onError(errorMsg);
    }
  };

  const stopScanning = async () => {
    if (scannerRef.current) {
      try {
        await scannerRef.current.stop();
        scannerRef.current = null;
        setIsScanning(false);
      } catch (err) {
        console.error('Error stopping scanner:', err);
      }
    }
  };

  useEffect(() => {
    return () => {
      if (scannerRef.current) {
        scannerRef.current.stop().catch(console.error);
      }
    };
  }, []);

  return (
    <div className="qr-scanner">
      <div id={elementId} style={{ width: '100%', maxWidth: '500px' }}></div>
      
      {error && (
        <div className="error-message" style={{ color: 'red', marginTop: '10px' }}>
          {error}
        </div>
      )}

      <div style={{ marginTop: '15px' }}>
        {!isScanning ? (
          <button onClick={startScanning} className="btn btn-primary">
            Start Camera
          </button>
        ) : (
          <button onClick={stopScanning} className="btn btn-danger">
            Stop Camera
          </button>
        )}
      </div>
    </div>
  );
}
