import React, { useState } from 'react';
import { Search } from 'lucide-react';
import './SearchBar.css';

export default function SearchBar({ onSearch, placeholder = "Search for a product (e.g. iPhone 16)..." }) {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) {
      setError('Please enter a product name to search');
      return;
    }
    setError('');
    onSearch(query.trim());
  };

  const handleInputChange = (e) => {
    setQuery(e.target.value);
    if (error && e.target.value.trim()) {
      setError('');
    }
  };

  return (
    <form className="search-bar-form" onSubmit={handleSubmit}>
      <div className={`search-input-wrapper ${error ? 'input-error' : ''}`}>
        <Search className="search-icon" size={20} />
        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          placeholder={placeholder}
          className="search-input"
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </div>
      {error && <span className="search-error-msg">{error}</span>}
    </form>
  );
}
