<script lang="ts">
    import { user } from './authStore';
    import { theme } from './design/themeStore';
    import { Mail, Lock, Eye, EyeClosed } from '@lucide/svelte';
    
    let email = '';
    let password = '';
    let error = '';
    let loading = false;
    let showPassword = false;

    const API_BASE_URL = 'http://localhost:5000';

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
                error = data.message || 'Login failed';
            }
        } catch (e) {
            error = 'Could not connect to server';
        } finally {
            loading = false;
        }
    }
</script>

<svelte:head>
    <title>AutoVault — Sign In</title>
    <meta name="description" content="Sign in to AutoVault — Secure File Versioning for PLC & CNC Programs." />
</svelte:head>

<div class="login-page">
    <div class="login-glow"></div>

    <div class="login-card">
        <div class="logo-section">
            <img src="/assets/logo-av-2.png" alt="AutoVault" class="logo" />
            <h1 class="brand">AutoVault</h1>
            <p class="tagline">Secure file versioning for machine programs</p>
        </div>

        <form on:submit|preventDefault={handleLogin}>
            <div class="input-group">
                <label for="login-email">Email</label>
                <div class="input-wrapper">
                    <Mail size={18} strokeWidth={1.75} />
                    <input
                        id="login-email"
                        type="email"
                        bind:value={email}
                        placeholder="you@company.com"
                        required
                        autocomplete="username"
                    />
                </div>
            </div>

            <div class="input-group">
                <label for="login-password">Password</label>
                <div class="input-wrapper">
                    <Lock size={18} strokeWidth={1.75} />
                    <input
                        id="login-password"
                        type={showPassword ? 'text' : 'password'}
                        bind:value={password}
                        placeholder="Enter your password"
                        required
                        autocomplete="current-password"
                    />
                    <button
                        type="button"
                        class="toggle-pw"
                        on:click={togglePasswordVisibility}
                        aria-label={showPassword ? 'Hide password' : 'Show password'}
                    >
                        {#if showPassword}
                            <EyeClosed size={16} strokeWidth={1.75} />
                        {:else}
                            <Eye size={16} strokeWidth={1.75} />
                        {/if}
                    </button>
                </div>
            </div>

            {#if error}
                <div class="error-msg">{error}</div>
            {/if}

            <button type="submit" class="submit-btn" disabled={loading}>
                {loading ? 'Signing in...' : 'Sign In'}
            </button>
        </form>

        <p class="footer-text">
            Secure · Versioned · Compliant
        </p>
    </div>
</div>

<style>
    .login-page {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100vw;
        height: 100vh;
        background: var(--color-canvas);
        position: relative;
        overflow: hidden;
    }

    .login-glow {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(94, 106, 210, 0.06) 0%, transparent 70%);
        pointer-events: none;
    }

    .login-card {
        position: relative;
        width: 100%;
        max-width: 400px;
        padding: var(--space-xl) var(--space-lg);
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-xl);
        animation: fadeUp 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .logo-section {
        text-align: center;
        margin-bottom: var(--space-xl);
    }

    .logo {
        height: 48px;
        width: auto;
        margin: 0 auto var(--space-md);
    }

    .brand {
        font-family: var(--font-display);
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.8px;
        color: var(--color-ink);
        margin: 0 0 var(--space-xxs);
    }

    .tagline {
        font-size: 14px;
        color: var(--color-ink-subtle);
        margin: 0;
    }

    form {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .input-group {
        display: flex;
        flex-direction: column;
        gap: var(--space-xxs);
    }

    .input-group label {
        font-size: 13px;
        font-weight: 500;
        color: var(--color-ink-subtle);
    }

    .input-wrapper {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: 0 var(--space-sm);
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        color: var(--color-ink-tertiary);
        transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
    }

    .input-wrapper:focus-within {
        border-color: var(--color-primary-focus);
        box-shadow: 0 0 0 2px rgba(94, 106, 210, 0.25);
    }

    .input-wrapper input {
        flex: 1;
        border: none;
        background: transparent;
        padding: 10px 0;
        font-size: 15px;
        color: var(--color-ink);
        outline: none;
        box-shadow: none;
    }

    .input-wrapper input::placeholder {
        color: var(--color-ink-tertiary);
    }

    .toggle-pw {
        all: unset;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4px;
        border-radius: var(--radius-xs);
        color: var(--color-ink-tertiary);
        cursor: pointer;
        transition: color var(--transition-fast);
    }

    .toggle-pw:hover {
        color: var(--color-ink-muted);
    }

    .error-msg {
        font-size: 13px;
        color: var(--color-error);
        text-align: center;
        padding: var(--space-xs) var(--space-sm);
        background: var(--color-error-subtle);
        border-radius: var(--radius-md);
    }

    .submit-btn {
        width: 100%;
        padding: 12px;
        background: var(--color-primary);
        color: var(--color-on-primary);
        border: none;
        border-radius: var(--radius-md);
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: background var(--transition-fast), transform var(--transition-fast);
        margin-top: var(--space-xs);
    }

    .submit-btn:hover:not(:disabled) {
        background: var(--color-primary-hover);
    }

    .submit-btn:active:not(:disabled) {
        transform: scale(0.98);
    }

    .submit-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .footer-text {
        text-align: center;
        font-size: 12px;
        color: var(--color-ink-tertiary);
        margin: var(--space-lg) 0 0;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (max-width: 480px) {
        .login-card {
            margin: var(--space-md);
            padding: var(--space-lg) var(--space-md);
        }
    }
</style>
