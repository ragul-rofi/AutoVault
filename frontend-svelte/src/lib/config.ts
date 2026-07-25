/**
 * API configuration for AutoVault Frontend.
 * Reads environment variable VITE_API_BASE_URL (set during build on Vercel)
 * and falls back to local backend URL http://localhost:5000.
 */
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000').replace(/\/$/, '');
