import React, { useState, useEffect } from 'react';
import { Globe, ChevronDown } from 'lucide-react';
import apiService from '../services/api';

const LanguageSelector = ({ selectedLanguage, onLanguageChange }) => {
  const [languages, setLanguages] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLanguages();
  }, []);

  const loadLanguages = async () => {
    try {
      const langs = await apiService.getLanguages();
      setLanguages(langs);
      
      // Set default language if not already set
      if (!selectedLanguage && langs.length > 0) {
        const defaultLang = langs.find(l => l.code === 'en') || langs[0];
        onLanguageChange(defaultLang.code, defaultLang.name);
      }
    } catch (error) {
      console.error('Error loading languages:', error);
      // Fallback languages
      const fallbackLangs = [
        { code: 'en', name: 'English' },
        { code: 'hi', name: 'Hindi' },
        { code: 'es', name: 'Spanish' },
      ];
      setLanguages(fallbackLangs);
      if (!selectedLanguage) {
        onLanguageChange('en', 'English');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageSelect = (lang) => {
    onLanguageChange(lang.code, lang.name);
    setIsOpen(false);
    
    // Save to localStorage
    localStorage.setItem('preferredLanguage', lang.code);
    localStorage.setItem('preferredLanguageName', lang.name);
  };

  const currentLanguage = languages.find(l => l.code === selectedLanguage) || 
    { code: 'en', name: 'English' };

  if (loading) {
    return (
      <div className="glass-effect rounded-full px-4 py-2 flex items-center gap-2">
        <Globe className="w-4 h-4 text-gray-400 animate-spin" />
        <span className="text-sm text-gray-600">Loading...</span>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Selected Language Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="glass-effect rounded-full px-4 py-2 flex items-center gap-2 hover:shadow-lg transition-all duration-300"
        aria-label="Select language"
        aria-expanded={isOpen}
      >
        <Globe className="w-4 h-4 text-primary-600" />
        <span className="text-sm font-medium text-gray-700">
          {currentLanguage.name}
        </span>
        <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setIsOpen(false)}
            aria-hidden="true"
          />
          
          {/* Menu */}
          <div className="absolute right-0 mt-2 w-56 glass-effect rounded-2xl shadow-xl z-20 overflow-hidden animate-fade-in">
            <div className="py-2 max-h-80 overflow-y-auto">
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => handleLanguageSelect(lang)}
                  className={`
                    w-full px-4 py-3 text-left text-sm transition-colors
                    ${lang.code === selectedLanguage 
                      ? 'bg-primary-50 text-primary-700 font-medium' 
                      : 'text-gray-700 hover:bg-gray-50'
                    }
                  `}
                >
                  <div className="flex items-center justify-between">
                    <span>{lang.name}</span>
                    {lang.code === selectedLanguage && (
                      <span className="text-primary-600">✓</span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default LanguageSelector;

