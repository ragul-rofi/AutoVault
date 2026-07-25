<script lang="ts">
    import { user } from './authStore';
    import { Mail, Lock, Eye, EyeClosed } from '@lucide/svelte';

    let email = '';
    let password = '';
    let error = '';
    let loading = false;
    let showPassword = false;

    import { API_BASE_URL } from './config';

    function togglePasswordVisibility() {
        showPassword = !showPassword;
    }

    async function handleLogin() {
        loading = true;
        error = '';
        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });
            const data = await response.json();
            if (response.ok && data.status === 'success') {
                user.set({
                    id: data.id,
                    name: data.name,
                    role: data.role
                });
            } else {
                error = data.message || 'Invalid credentials. Please try again.';
            }
        } catch (e) {
            error = 'Could not connect to server.';
        } finally {
            loading = false;
        }
    }
</script>

<svelte:head>
    <title>AutoVault — Login</title>
</svelte:head>

<div class="login-wrapper">
    <div class="login-card">
        <!-- Prominent AV Pixel Logo -->
        <div class="logo-container">
            <img src="/assets/logo-av-2.png" alt="AV Logo" class="av-logo" on:error={(e) => (e.currentTarget.src = '/assets/logo-av-2.png')} />
            <h1 class="welcome-title">Welcome Back</h1>
        </div>

        <form on:submit|preventDefault={handleLogin}>
            <!-- Clean Flat Email Input -->
            <div class="input-box">
                <Mail size={18} class="input-icon" />
                <input
                    type="email"
                    bind:value={email}
                    placeholder="email"
                    required
                    autocomplete="username"
                />
            </div>

            <!-- Clean Flat Password Input with Reveal -->
            <div class="input-box">
                <Lock size={18} class="input-icon" />
                <input
                    type={showPassword ? 'text' : 'password'}
                    bind:value={password}
                    placeholder="password"
                    required
                    autocomplete="current-password"
                />
                <button
                    type="button"
                    class="reveal-btn"
                    on:click={togglePasswordVisibility}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                    {#if showPassword}
                        <EyeClosed size={18} />
                    {:else}
                        <Eye size={18} />
                    {/if}
                </button>
            </div>

            {#if error}
                <div class="error-banner">{error}</div>
            {/if}

            <!-- Solid Black Login Button -->
            <button type="submit" class="login-btn" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
            </button>
        </form>
    </div>
</div>

<style>
    .login-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100vh;
        background: url('/assets/Login-bg.png') no-repeat center center fixed;
        background-size: cover;
        position: fixed;
        inset: 0;
        z-index: 9999;
    }

    .login-card {
        width: 100%;
        max-width: 360px;
        padding: 38px 32px 36px;
        background: url('/assets/Login-card-bg.png') no-repeat center center / cover,
                    linear-gradient(180deg, #ffffff 0%, #e2ebf8 45%, #9fc1f9 100%);
        border-radius: 16px;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        align-items: center;
        box-sizing: border-box;
        animation: cardAppear 250ms ease-out;
    }

    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 22px;
    }

    .av-logo {
        height: 64px;
        width: auto;
        margin-bottom: 14px;
        image-rendering: pixelated;
    }

    .welcome-title {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 26px;
        font-weight: 600;
        color: #000000;
        margin: 0;
        letter-spacing: -0.4px;
    }

    form {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 14px;
    }

    /* Flat Input Box - No Outer/Inner Highlighting Borders */
    .input-box {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0 14px;
        height: 48px;
        background: #ffffff;
        border: none;
        outline: none;
        border-radius: 8px;
        box-shadow: none;
        transition: none;
    }

    .input-box:focus-within {
        border: none;
        outline: none;
        box-shadow: none;
    }

    .input-box :global(.input-icon) {
        color: #1a1a1a;
        flex-shrink: 0;
    }

    .input-box input {
        flex: 1;
        border: none;
        outline: none;
        box-shadow: none;
        background: transparent;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 15px;
        color: #000000;
        padding: 0;
    }

    .input-box input:focus {
        border: none;
        outline: none;
        box-shadow: none;
    }

    .input-box input::placeholder {
        color: #8e8e93;
        font-size: 15px;
    }

    .reveal-btn {
        all: unset;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #8e8e93;
        cursor: pointer;
        transition: color 0.2s ease;
        padding: 2px;
    }

    .reveal-btn:hover {
        color: #000000;
    }

    .error-banner {
        font-size: 13px;
        color: #dc2626;
        background: rgba(220, 38, 38, 0.1);
        border-radius: 6px;
        padding: 8px 12px;
        text-align: center;
    }

    .login-btn {
        margin-top: 10px;
        height: 48px;
        width: 100%;
        background: #000000;
        color: #ffffff;
        border: none;
        outline: none;
        border-radius: 8px;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .login-btn:hover:not(:disabled) {
        background: #1a1a1a;
        transform: translateY(-1px);
    }

    .login-btn:active:not(:disabled) {
        transform: translateY(0);
    }

    .login-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    @keyframes cardAppear {
        from {
            opacity: 0;
            transform: scale(0.97);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
</style>
