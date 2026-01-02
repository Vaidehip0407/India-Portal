import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Home, User, FileText, Settings, LogOut, Zap, Flame, Droplets, Building,
  Menu, X, Bell, ChevronDown, Shield, HelpCircle
} from 'lucide-react';
import { useState } from 'react';

const Layout = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/services', icon: Settings, label: 'Services' },
    { path: '/applications', icon: FileText, label: 'My Applications' },
    { path: '/documents', icon: FileText, label: 'Documents' },
    { path: '/profile', icon: User, label: 'Profile' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          {/* Top Header */}
          <div className="flex justify-between items-center py-2 text-xs border-b border-blue-500">
            <div className="flex items-center gap-4">
              <span>🇮🇳 Government of Gujarat</span>
              <span className="hidden md:inline">|</span>
              <span className="hidden md:inline">गुजरात सरकार</span>
            </div>
            <div className="flex items-center gap-4">
              <button className="hover:text-orange-300">Skip to Content</button>
              <span>|</span>
              <button className="hover:text-orange-300">Screen Reader</button>
            </div>
          </div>
          
          {/* Main Header */}
          <div className="py-4 flex justify-between items-center">
            <div className="flex items-center gap-4">
              {/* Mobile Menu Toggle */}
              <button 
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 hover:bg-blue-500 rounded"
              >
                {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
              
              {/* Logo & Title */}
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg">
                  <Shield className="w-8 h-8 text-blue-600" />
                </div>
                <div>
                  <h1 className="text-xl md:text-2xl font-bold tracking-wide">
                    Unified Services Portal
                  </h1>
                  <p className="text-xs text-blue-200">एकीकृत सेवा पोर्टल | Gujarat State</p>
                </div>
              </div>
            </div>

            {/* Right Side */}
            <div className="flex items-center gap-3">
              {/* Service Icons */}
              <div className="hidden md:flex items-center gap-2 mr-4 px-4 py-2 bg-blue-500/50 rounded-lg">
                <Zap className="w-5 h-5 text-yellow-400" title="Electricity" />
                <Flame className="w-5 h-5 text-orange-400" title="Gas" />
                <Droplets className="w-5 h-5 text-cyan-400" title="Water" />
                <Building className="w-5 h-5 text-green-400" title="Property" />
              </div>

              {/* Notifications */}
              <button className="relative p-2 hover:bg-blue-500 rounded-full">
                <Bell className="w-5 h-5" />
                <span className="absolute top-0 right-0 w-2 h-2 bg-orange-500 rounded-full"></span>
              </button>

              {/* User Menu */}
              <div className="relative">
                <button 
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  className="flex items-center gap-2 px-3 py-2 bg-blue-500 hover:bg-blue-400 rounded-lg transition"
                >
                  <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center font-bold">
                    {user?.full_name?.charAt(0) || 'U'}
                  </div>
                  <span className="hidden md:inline">{user?.full_name || 'User'}</span>
                  <ChevronDown className="w-4 h-4" />
                </button>

                {userMenuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl py-2 z-50">
                    <Link 
                      to="/profile" 
                      className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-gray-100"
                      onClick={() => setUserMenuOpen(false)}
                    >
                      <User className="w-4 h-4" />
                      My Profile
                    </Link>
                    <Link 
                      to="/documents" 
                      className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-gray-100"
                      onClick={() => setUserMenuOpen(false)}
                    >
                      <FileText className="w-4 h-4" />
                      My Documents
                    </Link>
                    <hr className="my-2" />
                    <button
                      onClick={() => { logout(); setUserMenuOpen(false); }}
                      className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 w-full"
                    >
                      <LogOut className="w-4 h-4" />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? 'w-64' : 'w-0 lg:w-64'} bg-white shadow-xl min-h-[calc(100vh-140px)] transition-all duration-300 overflow-hidden`}>
          <nav className="p-4">
            {/* Quick Stats */}
            <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
              <p className="text-xs text-gray-500 mb-1">Welcome back,</p>
              <p className="font-semibold text-blue-900">{user?.full_name || 'User'}</p>
              <p className="text-xs text-gray-500 mt-2">{user?.email}</p>
            </div>

            {/* Navigation */}
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 px-4">
              Main Menu
            </p>
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl mb-1 transition-all ${
                  location.pathname === item.path
                    ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-blue-600'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            ))}

            {/* Help Section */}
            <div className="mt-8 p-4 bg-orange-50 rounded-xl border border-orange-200">
              <div className="flex items-center gap-2 text-orange-700 mb-2">
                <HelpCircle className="w-5 h-5" />
                <span className="font-semibold">Need Help?</span>
              </div>
              <p className="text-xs text-orange-600 mb-3">
                Contact our support team for assistance
              </p>
              <button className="w-full py-2 bg-orange-500 text-white rounded-lg text-sm font-medium hover:bg-orange-600 transition">
                Get Support
              </button>
            </div>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 min-h-[calc(100vh-140px)]">
          <Outlet />
        </main>
      </div>

      {/* Footer */}
      <footer className="bg-blue-700 text-white py-4">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm">
          <p>© 2024 Unified Services Portal | Government of Gujarat</p>
          <p className="text-blue-300 text-xs mt-1">
            Designed & Developed for Digital Gujarat Initiative
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
