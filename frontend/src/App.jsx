import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ProductProvider } from './context/ProductContext';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import Home from './pages/Home';
import Search from './pages/Search';
import Loading from './pages/Loading';
import Dashboard from './pages/Dashboard';
import ChartsPage from './pages/ChartsPage';
import Reviews from './pages/Reviews';
import NotFound from './pages/NotFound';
import './App.css';

export default function App() {
  return (
    <ProductProvider>
      <Router>
        <div className="app-layout">
          <Navbar />
          <main className="app-main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/search" element={<Search />} />
              <Route path="/loading" element={<Loading />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/charts" element={<ChartsPage />} />
              <Route path="/reviews" element={<Reviews />} />
              <Route path="/not-found" element={<NotFound />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </ProductProvider>
  );
}
