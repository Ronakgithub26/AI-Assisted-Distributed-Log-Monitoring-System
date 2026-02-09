import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  Phone,
  Calendar,
  UserPlus,
  ArrowRight,
  Sparkles,
  CheckCircle,
  XCircle,
  Brain,
  Globe,
} from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import "./Signup.css";

interface SignupFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  dob: string;
  gender: string;
  mobile: string;
  country: string;
  role: string;
  acceptTerms: boolean;
}

const Signup = () => {
  const [formData, setFormData] = useState<SignupFormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    dob: "",
    gender: "",
    mobile: "",
    country: "",
    role: "",
    acceptTerms: false,
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();
  const { signup, login } = useAuth();

  const roles = [
    { id: "admin", name: "Administrator", color: "from-red-500 to-pink-600" },
    { id: "manager", name: "Manager", color: "from-blue-500 to-cyan-600" },
    {
      id: "developer",
      name: "Developer",
      color: "from-green-500 to-emerald-600",
    },
    { id: "analyst", name: "Analyst", color: "from-purple-500 to-violet-600" },
    { id: "viewer", name: "Viewer", color: "from-gray-500 to-gray-600" },
  ];

  const genders = [
    { id: "male", name: "Male" },
    { id: "female", name: "Female" },
    { id: "other", name: "Other" },
    { id: "prefer-not-to-say", name: "Prefer not to say" },
  ];

  const countries = [
    "United States",
    "Canada",
    "United Kingdom",
    "Australia",
    "Germany",
    "France",
    "Japan",
    "India",
    "Brazil",
    "Singapore",
    "Other",
  ];

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value, type } = e.target;
    if (type === "checkbox") {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const validateForm = () => {
    if (!formData.username.trim()) return setError("Username is required");
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email))
      return setError("Please enter a valid email");
    if (formData.password.length < 8)
      return setError("Password must be at least 8 characters");
    if (formData.password !== formData.confirmPassword)
      return setError("Passwords do not match");
    if (!formData.dob) return setError("Date of birth is required");
    if (!formData.gender) return setError("Please select your gender");
    if (!formData.country) return setError("Please select your country");
    if (!formData.role) return setError("Please select a role");
    if (!formData.acceptTerms)
      return setError("You must accept the terms and conditions");
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!validateForm()) return;

    setLoading(true);
    try {
      const result = await signup(
        formData.email,
        formData.password,
        formData.username,
        formData.role,
        {
          dob: formData.dob,
          gender: formData.gender,
          mobile: formData.mobile,
          country: formData.country,
        },
      );

      if (result.success) {
        setSuccess(true);
        await login(formData.email, formData.password);
        setTimeout(() => navigate("/app/dashboard"), 3000);
      } else {
        setError(result.message || "Failed to create account");
      }
    } catch (err) {
      setError("An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoSignup = () => {
    const today = new Date();
    const birthDate = new Date(
      today.getFullYear() - 25,
      today.getMonth(),
      today.getDate(),
    );

    setFormData({
      username: "demo_user",
      email: "demo@logsentinel.ai",
      password: "Demo@2024",
      confirmPassword: "Demo@2024",
      dob: birthDate.toISOString().split("T")[0],
      gender: "male",
      mobile: "+1234567890",
      country: "United States",
      role: "admin",
      acceptTerms: true,
    });
  };

  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 },
  };

  const getSelectedRole = () => roles.find((role) => role.id === formData.role);

  if (success) {
    const selectedRole = getSelectedRole();
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="w-full max-w-md text-center"
        >
          <div className="mb-8">
            <div className="relative inline-block">
              <div
                className={`absolute inset-0 bg-gradient-to-r ${selectedRole?.color} rounded-full blur-xl opacity-50`}
              ></div>
              <div
                className={`relative w-24 h-24 bg-gradient-to-r ${selectedRole?.color} rounded-full flex items-center justify-center mx-auto mb-6`}
              >
                <CheckCircle className="w-12 h-12 text-white" />
              </div>
            </div>
            <h1 className="text-3xl font-bold text-white mb-4">
              Account Created Successfully!
            </h1>
            <p className="text-blue-200">
              Welcome,{" "}
              <span className="font-semibold text-white">
                {formData.username}
              </span>
              !
            </p>
          </div>

          <div className="bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-3xl border border-white/20 shadow-2xl p-8">
            <div className="text-left space-y-4 mb-8">
              <div className="flex items-center space-x-3">
                <User className="w-5 h-5 text-blue-400" />
                <div>
                  <p className="text-sm text-gray-400">Username</p>
                  <p className="text-white font-medium">{formData.username}</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-5 h-5 text-blue-400" />
                <div>
                  <p className="text-sm text-gray-400">Email</p>
                  <p className="text-white">{formData.email}</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <div
                  className={`w-10 h-10 rounded-lg bg-gradient-to-r ${selectedRole?.color} flex items-center justify-center`}
                >
                  <UserPlus className="w-5 h-5 text-white" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Role</p>
                  <p className="text-white font-medium">{selectedRole?.name}</p>
                </div>
              </div>
            </div>

            <div className="pt-6">
              <div className="flex items-center justify-center space-x-4 mb-6">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-green-400 font-medium">
                  Redirecting to dashboard...
                </span>
              </div>
              <Link
                to="/app/dashboard"
                className="inline-flex items-center justify-center w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl"
              >
                Go to Dashboard <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 p-4 relative overflow-hidden">
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
      </div>

      <motion.div
        {...fadeInUp}
        className="relative w-full max-w-2xl bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-3xl border border-white/20 shadow-2xl overflow-hidden"
      >
        <div className="p-8 md:p-12">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl blur opacity-75"></div>
                <div className="relative bg-gray-900 p-3 rounded-xl">
                  <Brain className="w-10 h-10 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">
                  Create Account
                </h1>
                <p className="text-blue-300 text-sm">
                  Simple & Secure Registration
                </p>
              </div>
            </div>
            <p className="text-blue-200">
              Join thousands of users monitoring their systems with AI
            </p>
          </div>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center space-x-3 p-4 rounded-xl bg-red-900/30 border border-red-800 text-red-200 mb-6"
            >
              <XCircle className="w-5 h-5 flex-shrink-0" />
              <span className="text-sm">{error}</span>
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label
                  htmlFor="username"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Username *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="username"
                    name="username"
                    type="text"
                    required
                    value={formData.username}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="johndoe"
                  />
                </div>
              </div>
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Email *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="john@example.com"
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Password *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    required
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full pl-10 pr-12 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="Create a strong password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-300" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400 hover:text-gray-300" />
                    )}
                  </button>
                </div>
              </div>
              <div>
                <label
                  htmlFor="confirmPassword"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Confirm Password *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    required
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className="w-full pl-10 pr-12 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="Confirm your password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-300" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400 hover:text-gray-300" />
                    )}
                  </button>
                </div>
                {formData.confirmPassword && (
                  <div className="mt-2 flex items-center space-x-2">
                    {formData.password === formData.confirmPassword ? (
                      <>
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span className="text-xs text-green-400">
                          Passwords match
                        </span>
                      </>
                    ) : (
                      <>
                        <XCircle className="w-4 h-4 text-red-500" />
                        <span className="text-xs text-red-400">
                          Passwords do not match
                        </span>
                      </>
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div>
                <label
                  htmlFor="dob"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Date of Birth *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Calendar className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="dob"
                    name="dob"
                    type="date"
                    required
                    value={formData.dob}
                    onChange={handleChange}
                    max={new Date().toISOString().split("T")[0]}
                    className="w-full pl-10 pr-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  />
                </div>
              </div>
              <div>
                <label
                  htmlFor="gender"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Gender *
                </label>
                <select
                  id="gender"
                  name="gender"
                  required
                  value={formData.gender}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                >
                  <option value="">Select gender</option>
                  {genders.map((gender) => (
                    <option key={gender.id} value={gender.id}>
                      {gender.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label
                  htmlFor="country"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Country *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Globe className="h-5 w-5 text-gray-400" />
                  </div>
                  <select
                    id="country"
                    name="country"
                    required
                    value={formData.country}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  >
                    <option value="">Select country</option>
                    {countries.map((country) => (
                      <option key={country} value={country}>
                        {country}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div>
                <label
                  htmlFor="mobile"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Mobile Number
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Phone className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="mobile"
                    name="mobile"
                    type="tel"
                    value={formData.mobile}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="+1 234 567 8900"
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label
                  htmlFor="role"
                  className="block text-sm font-medium text-blue-200 mb-2"
                >
                  Role *
                </label>
                <select
                  id="role"
                  name="role"
                  required
                  value={formData.role}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                >
                  <option value="">Select role</option>
                  {roles.map((role) => (
                    <option key={role.id} value={role.id}>
                      {role.name}
                    </option>
                  ))}
                </select>
                {formData.role && (
                  <div className="mt-2 flex items-center space-x-2">
                    <div
                      className={`w-3 h-3 rounded-full bg-gradient-to-r ${getSelectedRole()?.color}`}
                    ></div>
                    <span className="text-xs text-blue-300">
                      {getSelectedRole()?.name} role selected
                    </span>
                  </div>
                )}
              </div>
              <div className="flex items-end">
                <label className="flex items-center">
                  <input
                    id="acceptTerms"
                    name="acceptTerms"
                    type="checkbox"
                    checked={formData.acceptTerms}
                    onChange={handleChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-600 rounded bg-gray-800"
                  />
                  <span className="ml-2 text-sm text-blue-200">
                    I agree to the{" "}
                    <a
                      href="#"
                      className="text-blue-400 hover:text-blue-300 transition-colors"
                    >
                      Terms
                    </a>{" "}
                    and{" "}
                    <a
                      href="#"
                      className="text-blue-400 hover:text-blue-300 transition-colors"
                    >
                      Privacy Policy
                    </a>{" "}
                    *
                  </span>
                </label>
              </div>
            </div>

            <div className="space-y-4">
              <button
                type="submit"
                disabled={loading}
                className="w-full relative group"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition-opacity"></div>
                <div className="relative w-full flex items-center justify-center space-x-3 py-4 px-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl">
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span className="text-white font-semibold">
                        Creating Account...
                      </span>
                    </>
                  ) : (
                    <>
                      <span className="text-white font-semibold text-lg">
                        Create Account
                      </span>
                      <ArrowRight className="w-5 h-5" />
                    </>
                  )}
                </div>
              </button>

              <button
                type="button"
                onClick={handleDemoSignup}
                className="w-full flex items-center justify-center space-x-3 py-4 px-6 bg-gradient-to-r from-gray-800 to-gray-900 hover:from-gray-900 hover:to-black border border-gray-700 rounded-xl text-white font-semibold transition-all duration-200 hover:shadow-lg"
              >
                <Sparkles className="w-5 h-5" />
                <span>Try Demo with Admin Role</span>
              </button>
            </div>
          </form>

          <div className="mt-8 text-center">
            <p className="text-blue-200">
              Already have an account?{" "}
              <Link
                to="/login"
                className="text-blue-400 hover:text-blue-300 font-semibold transition-colors"
              >
                Sign in here
              </Link>
            </p>
          </div>

          <div className="mt-8 p-4 bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-xl border border-blue-800/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white font-semibold">14-Day Free Trial</p>
                <p className="text-blue-300 text-sm">
                  Full access to all features
                </p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-white">$0</p>
                <p className="text-blue-300 text-sm">Professional Plan</p>
              </div>
            </div>
          </div>
        </div>

        <div className="px-8 py-4 bg-gradient-to-r from-blue-900/30 via-purple-900/30 to-pink-900/30 border-t border-white/10">
          <div className="flex flex-wrap items-center justify-center gap-6">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-blue-400" />
              <span className="text-xs text-gray-400">Secure Registration</span>
            </div>
            <div className="h-4 w-px bg-gray-700"></div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span className="text-xs text-gray-400">
                No credit card needed
              </span>
            </div>
            <div className="h-4 w-px bg-gray-700"></div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs text-gray-400">Cancel anytime</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Signup;
