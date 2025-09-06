import React from "react";
import { Link } from "react-router-dom";
import { FaRobot, FaShieldAlt, FaChartLine, FaComments } from "react-icons/fa";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const HomePage = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50 transition-colors duration-300">
      <Navbar />

      {/* Hero Section */}
      <main className="flex-1 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-800 text-white pt-24">
        <div className="container mx-auto px-4 py-12 sm:py-20 lg:py-24">
          <div className="text-center max-w-4xl mx-auto">
            {/* Main Icon */}
            <div className="mb-8">
              <FaRobot className="text-5xl sm:text-6xl lg:text-7xl mx-auto text-yellow-300 animate-pulse" />
            </div>

            {/* Main Heading */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold mb-6 leading-tight animate-fadeIn">
              Welcome to <span className="text-yellow-300">FinSathi AI</span>
            </h1>

            {/* Subtitle */}
            <p className="text-lg sm:text-xl lg:text-2xl mb-8 opacity-90 max-w-3xl mx-auto leading-relaxed animate-fadeIn">
              Your Financial Buddy – Ask about banking terms, loans, fraud
              alerts, and online security with confidence.
            </p>

            {/* Features Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 mb-10">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 hover:bg-white/20 transition-all duration-300 border border-white/20">
                <FaShieldAlt className="text-3xl sm:text-4xl mx-auto mb-3 text-green-400" />
                <h3 className="text-lg sm:text-xl font-semibold mb-2 text-white">Secure & Private</h3>
                <p className="text-sm sm:text-base text-white/80">Your data is protected with enterprise-grade security</p>
              </div>

              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 hover:bg-white/20 transition-all duration-300 border border-white/20">
                <FaChartLine className="text-3xl sm:text-4xl mx-auto mb-3 text-blue-400" />
                <h3 className="text-lg sm:text-xl font-semibold mb-2 text-white">Financial Insights</h3>
                <p className="text-sm sm:text-base text-white/80">Get expert advice on complex financial topics</p>
              </div>

              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 hover:bg-white/20 transition-all duration-300 sm:col-span-2 lg:col-span-1 border border-white/20">
                <FaComments className="text-3xl sm:text-4xl mx-auto mb-3 text-purple-400" />
                <h3 className="text-lg sm:text-xl font-semibold mb-2 text-white">24/7 Support</h3>
                <p className="text-sm sm:text-base text-white/80">Always available to help with your queries</p>
              </div>
            </div>

            {/* CTA Button */}
            <Link
              to="/chat"
              className="inline-block bg-white text-indigo-600 px-8 sm:px-10 py-4 sm:py-5 rounded-full font-bold text-lg sm:text-xl hover:bg-gray-100 hover:scale-105 transition-all duration-300 shadow-2xl"
            >
              Start Your Financial Chat →
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default HomePage;
