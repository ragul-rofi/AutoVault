<script lang="ts">
    import { user } from '../authStore';
    import { theme, toggleTheme } from '../design/themeStore';
    import { Sun, Moon, User, Lock, Bell, Key } from '@lucide/svelte';

    export let showToast: (msg: string, type: 'success' | 'error' | 'warning' | 'info') => void = () => {};

    let currentPassword = '';
    let newPassword = '';
    let confirmPassword = '';

    function handlePasswordChange() {
        if (!currentPassword || !newPassword || !confirmPassword) {
            showToast('Please fill all password fields', 'error');
            return;
        }
        if (newPassword !== confirmPassword) {
            showToast('Passwords do not match', 'error');
            return;
        }
        showToast('Password changed successfully', 'success');
        currentPassword = ''; newPassword = ''; confirmPassword = '';
    }
</script>

<div class="settings-page">
    <!-- Profile -->
    <div class="card">
        <div class="card-header">
            <h3><User size={18} /> Profile</h3>
        </div>
        <div class="profile-grid">
            <div class="form-group">
                <label>Name</label>
                <input type="text" value={$user?.name || ''} disabled />
            </div>
            <div class="form-group">
                <label>Role</label>
                <input type="text" value={$user?.role || ''} disabled />
            </div>
        </div>
    </div>

    <!-- Appearance -->
    <div class="card">
        <div class="card-header">
            <h3>{#if $theme === 'dark'}<Moon size={18} />{:else}<Sun size={18} />{/if} Appearance</h3>
        </div>
        <div class="theme-picker">
            <button class="theme-option" class:active={$theme === 'dark'} on:click={() => theme.set('dark')}>
                <Moon size={20} />
                <span>Dark</span>
            </button>
            <button class="theme-option" class:active={$theme === 'light'} on:click={() => theme.set('light')}>
                <Sun size={20} />
                <span>Light</span>
            </button>
        </div>
    </div>

    <!-- Password -->
    <div class="card">
        <div class="card-header">
            <h3><Lock size={18} /> Change Password</h3>
        </div>
        <form on:submit|preventDefault={handlePasswordChange} class="password-form">
            <div class="form-group">
                <label>Current Password</label>
                <input type="password" bind:value={currentPassword} placeholder="Enter current password" />
            </div>
            <div class="form-group">
                <label>New Password</label>
                <input type="password" bind:value={newPassword} placeholder="Enter new password" />
            </div>
            <div class="form-group">
                <label>Confirm New Password</label>
                <input type="password" bind:value={confirmPassword} placeholder="Confirm new password" />
            </div>
            <button type="submit" class="primary-btn">Update Password</button>
        </form>
    </div>
</div>

<style>
    .settings-page { display: grid; gap: var(--space-lg); max-width: 600px; }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }
    .card-header { margin-bottom: var(--space-lg); }
    .card-header h3 {
        font-size: 16px; font-weight: 600; color: var(--color-ink); margin: 0;
        display: flex; align-items: center; gap: var(--space-xs);
    }

    .profile-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md); }

    .form-group label {
        display: block; font-size: 13px; font-weight: 500;
        color: var(--color-ink-subtle); margin-bottom: var(--space-xs);
    }

    .form-group input:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .theme-picker {
        display: flex;
        gap: var(--space-md);
    }

    .theme-option {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--space-xs);
        padding: var(--space-lg) var(--space-xl);
        background: var(--color-surface-2);
        border: 2px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        color: var(--color-ink-subtle);
        cursor: pointer;
        transition: all var(--transition-fast);
        font-size: 14px;
        font-weight: 500;
        flex: 1;
    }

    .theme-option:hover {
        border-color: var(--color-hairline-strong);
        color: var(--color-ink);
    }

    .theme-option.active {
        border-color: var(--color-primary);
        color: var(--color-primary);
        background: rgba(94, 106, 210, 0.06);
    }

    .password-form {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .primary-btn {
        padding: 10px 20px; background: var(--color-primary); color: var(--color-on-primary);
        border: none; border-radius: var(--radius-md); font-size: 14px; font-weight: 500;
        cursor: pointer; align-self: flex-start;
        transition: background var(--transition-fast);
    }
    .primary-btn:hover { background: var(--color-primary-hover); }

    @media (max-width: 480px) {
        .profile-grid { grid-template-columns: 1fr; }
    }
</style>
