import React from "react";
import {
  FaGithub,
  FaLinkedin,
  FaEnvelope,
  FaDiscord,
  FaHeart,
  FaRocket,
} from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="relative overflow-hidden border-t border-gray-200 dark:border-gray-800 bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-950">
      {/* Decorative top gradient bar */}
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-80" />

      {/* Soft glow blobs */}
      <div className="pointer-events-none absolute -top-10 -right-20 h-40 w-40 rounded-full blur-3xl opacity-20 bg-blue-400"></div>
      <div className="pointer-events-none absolute -bottom-16 -left-16 h-48 w-48 rounded-full blur-3xl opacity-10 bg-purple-500"></div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Brand */}
        <div className="text-center mb-8">
          <div className="flex justify-center items-center mb-4">
            <FaRocket className="text-blue-600 dark:text-yellow-300 text-3xl mr-3 animate-bounce" />
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">FinSathi AI</h3>
          </div>
          <p className="text-gray-600 dark:text-gray-400 max-w-xl mx-auto">
            Empowering your financial journey with clear, cited insights and guidance.
          </p>
        </div>

        {/* Socials */}
        <div className="flex justify-center flex-wrap gap-4 sm:gap-6 mb-8">
          <a
            href="https://github.com/Madhav-P-2005"
            target="_blank"
            rel="noopener noreferrer"
            className="group inline-flex items-center justify-center h-11 w-11 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow hover:shadow-md transition-all"
            aria-label="GitHub"
          >
            <FaGithub className="text-gray-700 dark:text-gray-200 group-hover:scale-110 transition-transform" size={20} />
          </a>
          <a
            href="https://www.linkedin.com/in/madhav-p-156b9b290/"
            target="_blank"
            rel="noopener noreferrer"
            className="group inline-flex items-center justify-center h-11 w-11 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow hover:shadow-md transition-all"
            aria-label="LinkedIn"
          >
            <FaLinkedin className="text-blue-600 group-hover:scale-110 transition-transform" size={20} />
          </a>
          <a
            href="mailto:madhavp2023@gmail.com"
            className="group inline-flex items-center justify-center h-11 w-11 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow hover:shadow-md transition-all"
            aria-label="Email"
          >
            <FaEnvelope className="text-red-500 group-hover:scale-110 transition-transform" size={20} />
          </a>
          <a
            href="https://discord.com/users/madhav"
            target="_blank"
            rel="noopener noreferrer"
            className="group inline-flex items-center justify-center h-11 w-11 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow hover:shadow-md transition-all"
            aria-label="Discord"
          >
            <FaDiscord className="text-indigo-500 group-hover:scale-110 transition-transform" size={20} />
          </a>
        </div>

        {/* Credits */}
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 text-gray-600 dark:text-gray-400">
            <span>Developed by</span>
            <span className="font-semibold text-gray-900 dark:text-gray-100">Madhav P</span>
            <span>with</span>
            <FaHeart className="text-red-500 animate-pulse" />
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
            © {new Date().getFullYear()} FinSathi AI. Built for financial empowerment.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
