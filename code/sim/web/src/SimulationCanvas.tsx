import { useRef, useEffect } from 'react';
import type { Entity } from './types';

interface SimulationCanvasProps {
  entities: Entity[];
  selectedEntity: Entity | null;
  onEntityClick: (entity: Entity | null) => void;
}

const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const ENTITY_RADIUS = 20;

export function SimulationCanvas({ entities, selectedEntity, onEntityClick }: SimulationCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // Draw grid
    ctx.strokeStyle = '#e9ecef';
    ctx.lineWidth = 1;
    for (let x = 0; x < CANVAS_WIDTH; x += 50) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, CANVAS_HEIGHT);
      ctx.stroke();
    }
    for (let y = 0; y < CANVAS_HEIGHT; y += 50) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(CANVAS_WIDTH, y);
      ctx.stroke();
    }

    // Draw entities
    entities.forEach((entity) => {
      ctx.save();

      // Shadow
      ctx.shadowColor = 'rgba(0, 0, 0, 0.2)';
      ctx.shadowBlur = 10;
      ctx.shadowOffsetX = 2;
      ctx.shadowOffsetY = 2;

      // Circle
      ctx.beginPath();
      ctx.arc(entity.x, entity.y, ENTITY_RADIUS, 0, Math.PI * 2);
      ctx.fillStyle = entity.type === 'person' ? '#3b82f6' : '#10b981';
      ctx.fill();

      // Selection outline
      if (selectedEntity && selectedEntity.id === entity.id) {
        ctx.strokeStyle = '#f7931a';
        ctx.lineWidth = 3;
        ctx.stroke();
      }

      ctx.shadowColor = 'transparent';

      // Icon
      ctx.fillStyle = 'white';
      ctx.font = 'bold 20px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(entity.type === 'person' ? '👤' : '🏪', entity.x, entity.y);

      // BTC amount
      ctx.fillStyle = '#333';
      ctx.font = '10px Arial';
      ctx.fillText(entity.btc.toFixed(3), entity.x, entity.y + 30);

      ctx.restore();
    });
  }, [entities, selectedEntity]);

  const handleClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Find clicked entity
    let clickedEntity: Entity | null = null;
    for (let i = entities.length - 1; i >= 0; i--) {
      const entity = entities[i];
      const dx = entity.x - x;
      const dy = entity.y - y;
      if (Math.sqrt(dx * dx + dy * dy) < ENTITY_RADIUS) {
        clickedEntity = entity;
        break;
      }
    }

    onEntityClick(clickedEntity);
  };

  return (
    <div style={{ background: '#f8f9fa', borderRadius: '8px', padding: '10px', display: 'flex', justifyContent: 'center' }}>
      <canvas
        ref={canvasRef}
        width={CANVAS_WIDTH}
        height={CANVAS_HEIGHT}
        onClick={handleClick}
        style={{
          border: '2px solid #dee2e6',
          borderRadius: '4px',
          background: 'white',
          cursor: 'crosshair',
        }}
      />
    </div>
  );
}
