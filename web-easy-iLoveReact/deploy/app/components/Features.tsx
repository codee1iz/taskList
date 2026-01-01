'use client';

interface Feature {
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    title: 'ELITE HACKING SKILLS',
    description: 'Профессиональные инструменты для проникновения в любые системы. Работаем быстро, тихо, эффективно.'
  },
  {
    title: 'ANONYMOUS OPERATIONS',
    description: 'Полная анонимность и безопасность. Ваша личность останется в секрете, даже если нас поймают.'
  },
  {
    title: '24/7 AVAILABILITY',
    description: 'Работаем круглосуточно. Хакеры не спят, они взламывают. Мы всегда на связи для ваших нужд.'
  },
  {
    title: 'GUARANTEED RESULTS',
    description: '100% гарантия успеха или возврат денег. Мы не останавливаемся, пока не достигнем цели.'
  }
];

export default function Features() {
  return (
    <div className="features">
      {features.map((feature, index) => (
        <div key={index} className="feature-card">
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </div>
      ))}
    </div>
  );
}

