import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaRobot } from 'react-icons/fa';

const Navbar = () => {

  useEffect(() => {
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const enableDark = saved ? saved === 'dark' : prefersDark;
    document.documentElement.classList.toggle('dark', enableDark);
  }, []);

  return (
    <nav className="fixed top-4 left-1/2 transform -translate-x-1/2 w-[95%] max-w-4xl bg-white/80 dark:bg-gray-900/70 backdrop-blur-md border border-gray-200 dark:border-gray-700 rounded-2xl shadow-lg z-50">
      <div className="px-4 sm:px-6 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-3 group">
          <FaRobot className="text-blue-600 dark:text-yellow-300 text-2xl group-hover:rotate-12 transition-transform duration-300" />
          <span className="text-lg sm:text-xl font-bold text-gray-800 dark:text-gray-100">FinSathi AI</span>
        </div>
        <div className="flex items-center gap-2 sm:gap-3">
          <Link to="/chat" className="bg-blue-600 text-white px-4 sm:px-5 py-2 rounded-full font-semibold hover:bg-blue-700 hover:scale-105 transition-all duration-300 shadow-md">
            Get Started
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
