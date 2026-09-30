import React, { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { LayoutDashboard, Menu, X, MessageSquare, Search, Home as HomeIcon, PieChart } from 'lucide-react';
import './Navbar.css';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);
  const closeMenu = () => setIsOpen(false);

  return (
    <header className="navbar-header glass-panel">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo" onClick={closeMenu}>
          <PieChart className="logo-icon" />
          <span className="logo-text">Sentima<span className="logo-dot">.</span></span>
        </Link>

        <nav className="navbar-desktop">
          <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            <HomeIcon size={16} /> Home
          </NavLink>
          <NavLink to="/search" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            <Search size={16} /> Search
          </NavLink>
          <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            <LayoutDashboard size={16} /> Dashboard
          </NavLink>
          <NavLink to="/charts" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            <PieChart size={16} /> Charts
          </NavLink>
          <NavLink to="/reviews" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            <MessageSquare size={16} /> Reviews
          </NavLink>
        </nav>

        <button className="navbar-toggle" onClick={toggleMenu} aria-label="Toggle navigation menu">
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      <div className={`navbar-mobile ${isOpen ? 'open' : ''}`}>
        <nav className="navbar-mobile-links">
          <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={closeMenu}>
            <HomeIcon size={18} /> Home
          </NavLink>
          <NavLink to="/search" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={closeMenu}>
            <Search size={18} /> Search
          </NavLink>
          <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={closeMenu}>
            <LayoutDashboard size={18} /> Dashboard
          </NavLink>
          <NavLink to="/charts" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={closeMenu}>
            <PieChart size={18} /> Charts
          </NavLink>
          <NavLink to="/reviews" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={closeMenu}>
            <MessageSquare size={18} /> Reviews
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
