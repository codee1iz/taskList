'use client';

export default function Header() {
  return (
    <header>
      <h1 className="glitch-text">HACKER MODE: ACTIVATED</h1>
      <p className="subtitle">[ ACCESS GRANTED ]</p>
      <div className="ascii-art">
        {`    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝`}
      </div>
    </header>
  );
}

