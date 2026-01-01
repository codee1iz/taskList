import Scanline from './components/Scanline';
import MatrixBackground from './components/MatrixBackground';
import Header from './components/Header';
import Terminal from './components/Terminal';
import Stats from './components/Stats';
import Features from './components/Features';
import HackButton from './components/HackButton';
import Warning from './components/Warning';
import Footer from './components/Footer';

export default function Home() {
  return (
    <>
      <Scanline />
      <MatrixBackground />
      <div className="container">
        <Header />
        <Terminal />
        <Stats />
        <Features />
        <HackButton />
        <Warning />
        <Footer />
      </div>
    </>
  );
}
