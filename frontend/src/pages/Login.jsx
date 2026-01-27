import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, LogIn, Shield, Zap, Flame, Droplets, Building } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    console.log('Sending login request:', { email, password: '***' });
    
    const result = await login(email, password);
    
    console.log('Login result:', result);
    
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
      console.error('Login failed:', result.error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex flex-col">
      {/* Top Strip */}
      <div className="h-1 bg-blue-500"></div>
      
      {/* Header */}
      <div className="text-center py-8">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-lg border-2 border-gray-200">
            <img src="/ashoka-emblem.webp" alt="Ashoka Emblem" className="w-14 h-14 object-contain" />
          </div>
        </div>
        <div className="flex justify-center gap-3 mb-3">
          <Zap className="w-6 h-6 text-yellow-600" />
          <Flame className="w-6 h-6 text-orange-600" />
          <Droplets className="w-6 h-6 text-blue-600" />
          <Building className="w-6 h-6 text-green-600" />
        </div>
        <h1 className="text-2xl font-bold text-gray-800">Unified Services Portal</h1>
        
      </div>

      {/* Login Card */}
      <div className="flex-1 flex items-center justify-center px-4 pb-10">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
            {/* Card Header - Blue Background */}
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-8 py-6 text-white text-center">
              <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="w-8 h-8" />
              </div>
              <h2 className="text-2xl font-bold">Citizen Login</h2>
              <p className="text-blue-100 text-sm mt-1">નાગરિક લૉગિન</p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="p-8 space-y-5">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
                  Login failed. Please try again.
                </div>
              )}

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none transition-all duration-300 hover:border-gray-300 bg-gray-50"
                    placeholder="Enter your email"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none transition-all duration-300 hover:border-gray-300 bg-gray-50"
                    placeholder="Enter your password"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition-colors flex items-center justify-center gap-2 shadow-sm disabled:opacity-50"
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <>
                    <LogIn className="w-5 h-5" />
                    Login to Portal
                  </>
                )}
              </button>

              <div className="text-center pt-4 border-t border-gray-100">
                <p className="text-gray-600">
                  Don't have an account?{' '}
                  <Link to="/register" className="text-blue-600 font-semibold hover:text-blue-700 transition-colors duration-300 hover:underline">
                    Register Now
                  </Link>
                </p>
              </div>

              {/* Test Credentials */}
              <div className="mt-4 p-3 bg-gray-50 rounded-lg text-center">
                <p className="text-xs text-gray-600">
                  <strong>Test Account:</strong><br />
                  Email: test@example.com<br />
                  Password: test123
                </p>
              </div>
            </form>
          </div>

          {/* Footer */}
          <div className="text-center mt-6 text-gray-600 text-sm">
            <p>🇮🇳 Government of India | સત્યમેવ જયતે</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
