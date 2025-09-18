import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="header">
      <h1>Road App</h1>
      <nav className="header-nav">
        <Link to="/">Map</Link>
        <Link to="/about">About</Link>
      </nav>
    </header>
  );
};

export default Header;