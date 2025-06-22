import { useEffect, useRef } from 'react';

export default function GridBackground({ darkMode }: { darkMode: boolean }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const handleMove = (e: MouseEvent) => {
      const xRatio = (e.clientX / window.innerWidth - 0.5) * 10;
      el.style.transform = `perspective(800px) rotateX(70deg) rotateY(${xRatio}deg)`;
    };
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return (
    <div
      ref={ref}
      className={`grid-bg ${darkMode ? 'dark' : 'light'}`}
      aria-hidden="true"
    />
  );
}

