import { useState, useRef } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

export type PipelineStep = {
  id: number;
  sql: string;
};

function DraggableStep({ step, index, moveStep }: { step: PipelineStep; index: number; moveStep: (from: number, to: number) => void }) {
  const ref = useRef<HTMLDivElement>(null);
  const [, drop] = useDrop({
    accept: 'STEP',
    hover(item: { index: number }) {
      if (!ref.current || item.index === index) return;
      moveStep(item.index, index);
      item.index = index;
    },
  });
  const [{ isDragging }, drag] = useDrag({
    type: 'STEP',
    item: { index },
    collect: (monitor) => ({ isDragging: monitor.isDragging() }),
  });
  drag(drop(ref));
  return (
    <div ref={ref} style={{ opacity: isDragging ? 0.5 : 1, padding: 8, marginBottom: 4, border: '1px solid var(--border)', borderRadius: 4, background: 'var(--panel)' }}>
      <strong>{step.sql.split(/\s+/)[0].toUpperCase()}</strong> - {step.sql}
    </div>
  );
}

export default function PipelineBuilder({ steps, onChange }: { steps: PipelineStep[]; onChange: (s: PipelineStep[]) => void }) {
  const moveStep = (from: number, to: number) => {
    const updated = [...steps];
    const [removed] = updated.splice(from, 1);
    updated.splice(to, 0, removed);
    onChange(updated);
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div>
        {steps.map((s, i) => (
          <DraggableStep key={s.id} step={s} index={i} moveStep={moveStep} />
        ))}
      </div>
    </DndProvider>
  );
}
