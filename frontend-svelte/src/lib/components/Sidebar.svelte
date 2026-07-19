<script lang="ts">
    import { user } from '../authStore';
    import { theme, toggleTheme } from '../design/themeStore';
    import {
        LayoutDashboard, Upload, List, RotateCcw, ArrowLeftRight,
        LogOut, User, Settings, BarChart3, Users, Shield,
        Sun, Moon, ChevronLeft, Activity
    } from '@lucide/svelte';

    export let activeTab: string = 'overview';
    export let onTabChange: (tab: string) => void = () => {};
    export let onLogout: () => void = () => {};

    let collapsed = false;

    interface NavItem {
        id: string;
        label: string;
        icon: any;
        adminOnly?: boolean;
    }

    const navItems: NavItem[] = [
        { id: 'overview', label: 'Overview', icon: LayoutDashboard },
        { id: 'upload', label: 'Upload', icon: Upload },
        { id: 'view', label: 'Files', icon: List },
        { id: 'rollback', label: 'Rollback', icon: RotateCcw, adminOnly: true },
        { id: 'compare', label: 'Compare', icon: ArrowLeftRight, adminOnly: true },
        { id: 'machines', label: 'Machines', icon: Settings },
        { id: 'analytics', label: 'Analytics', icon: BarChart3 },
        { id: 'audit', label: 'Audit Trail', icon: Activity },
        { id: 'access', label: 'Access Control', icon: Users, adminOnly: true },
        { id: 'settings', label: 'Settings', icon: Shield },
    ];

    $: visibleItems = navItems.filter(item => !item.adminOnly || $user?.role === 'admin');

    function handleTabClick(id: string) {
        onTabChange(id);
    }
</script>

<aside class="sidebar" class:collapsed>
    <div class="sidebar-header">
        {#if !collapsed}
            <img src="/assets/logo-av-2.png" alt="AutoVault" class="sidebar-logo" />
            <span class="sidebar-brand">AutoVault</span>
        {:else}
            <img src="/assets/logo-av-2.png" alt="AV" class="sidebar-logo mini" />
        {/if}
    </div>

    <nav class="sidebar-nav">
        {#each visibleItems as item}
            <button
                class="nav-item"
                class:active={activeTab === item.id}
                on:click={() => handleTabClick(item.id)}
                title={collapsed ? item.label : ''}
            >
                <svelte:component this={item.icon} size={18} />
                {#if !collapsed}
                    <span class="nav-label">{item.label}</span>
                {/if}
            </button>
        {/each}
    </nav>

    <div class="sidebar-footer">
        <button class="theme-toggle" on:click={toggleTheme} title={$theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}>
            {#if $theme === 'dark'}
                <Sun size={16} />
            {:else}
                <Moon size={16} />
            {/if}
            {#if !collapsed}
                <span>{$theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
            {/if}
        </button>

        <div class="user-pill">
            <div class="user-avatar">
                <User size={14} />
            </div>
            {#if !collapsed}
                <div class="user-info">
                    <span class="user-name">{$user?.name}</span>
                    <span class="user-role">{$user?.role}</span>
                </div>
            {/if}
        </div>

        <button class="logout-btn" on:click={onLogout} title="Logout">
            <LogOut size={14} />
            {#if !collapsed}
                <span>Logout</span>
            {/if}
        </button>
    </div>

    <button class="collapse-toggle" on:click={() => collapsed = !collapsed} title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}>
        <ChevronLeft size={14} class={collapsed ? 'rotated' : ''} />
    </button>
</aside>

<style>
    .sidebar {
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        width: var(--sidebar-width);
        background: var(--color-surface-1);
        border-right: 1px solid var(--color-hairline);
        display: flex;
        flex-direction: column;
        z-index: 50;
        transition: width var(--transition-slow);
        overflow: hidden;
    }

    .sidebar.collapsed {
        width: var(--sidebar-collapsed);
    }

    .sidebar-header {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-lg) var(--space-md);
        min-height: var(--topbar-height);
    }

    .sidebar-logo {
        height: 28px;
        width: auto;
        flex-shrink: 0;
    }

    .sidebar-logo.mini {
        height: 22px;
    }

    .sidebar-brand {
        font-family: var(--font-display);
        font-size: 16px;
        font-weight: 700;
        letter-spacing: -0.4px;
        color: var(--color-ink);
        white-space: nowrap;
    }

    .sidebar-nav {
        flex: 1;
        padding: var(--space-xs);
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        width: 100%;
        padding: 10px var(--space-sm);
        border: none;
        background: transparent;
        color: var(--color-ink-subtle);
        font-size: 14px;
        font-weight: 500;
        text-align: left;
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all var(--transition-fast);
        white-space: nowrap;
        position: relative;
    }

    .nav-item:hover {
        background: var(--color-surface-2);
        color: var(--color-ink-muted);
    }

    .nav-item.active {
        background: var(--color-surface-2);
        color: var(--color-ink);
    }

    .nav-item.active::before {
        content: '';
        position: absolute;
        left: 0;
        top: 6px;
        bottom: 6px;
        width: 3px;
        border-radius: 0 var(--radius-xs) var(--radius-xs) 0;
        background: var(--color-primary);
    }

    .nav-item :global(svg) {
        flex-shrink: 0;
        opacity: 0.7;
    }

    .nav-item.active :global(svg) {
        opacity: 1;
        color: var(--color-primary);
    }

    .nav-label {
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .sidebar-footer {
        padding: var(--space-sm);
        border-top: 1px solid var(--color-hairline);
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .theme-toggle {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        padding: 8px var(--space-sm);
        border: none;
        background: transparent;
        color: var(--color-ink-subtle);
        font-size: 13px;
        font-weight: 500;
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all var(--transition-fast);
        white-space: nowrap;
        width: 100%;
        justify-content: flex-start;
    }

    .theme-toggle:hover {
        background: var(--color-surface-2);
        color: var(--color-ink-muted);
    }

    .user-pill {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        padding: var(--space-xs);
        background: var(--color-surface-2);
        border-radius: var(--radius-md);
    }

    .user-avatar {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: var(--color-primary);
        color: var(--color-on-primary);
        border-radius: var(--radius-full);
        flex-shrink: 0;
    }

    .user-info {
        display: flex;
        flex-direction: column;
        min-width: 0;
    }

    .user-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--color-ink);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .user-role {
        font-size: 11px;
        color: var(--color-ink-subtle);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .logout-btn {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        padding: 8px var(--space-sm);
        border: 1px solid var(--color-hairline);
        background: transparent;
        color: var(--color-ink-subtle);
        font-size: 13px;
        font-weight: 500;
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all var(--transition-fast);
        white-space: nowrap;
        width: 100%;
        justify-content: flex-start;
    }

    .logout-btn:hover {
        background: var(--color-error-subtle);
        color: var(--color-error);
        border-color: var(--color-error);
    }

    .collapse-toggle {
        position: absolute;
        top: 50%;
        right: -12px;
        transform: translateY(-50%);
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-full);
        color: var(--color-ink-subtle);
        cursor: pointer;
        z-index: 51;
        opacity: 0;
        transition: all var(--transition-fast);
    }

    .sidebar:hover .collapse-toggle {
        opacity: 1;
    }

    .collapse-toggle:hover {
        background: var(--color-surface-2);
        color: var(--color-ink);
    }

    .collapse-toggle :global(.rotated) {
        transform: rotate(180deg);
    }

    @media (max-width: 1024px) {
        .sidebar {
            width: var(--sidebar-collapsed);
        }
        .sidebar-brand, .nav-label, .user-info, .theme-toggle span, .logout-btn span {
            display: none;
        }
        .collapse-toggle {
            display: none;
        }
    }

    @media (max-width: 768px) {
        .sidebar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            top: auto;
            width: 100% !important;
            height: auto;
            flex-direction: row;
            border-right: none;
            border-top: 1px solid var(--color-hairline);
            padding: var(--space-xs);
        }

        .sidebar-header,
        .sidebar-footer,
        .collapse-toggle {
            display: none;
        }

        .sidebar-nav {
            flex-direction: row;
            padding: 0;
            gap: 0;
            overflow-x: auto;
            justify-content: space-around;
        }

        .nav-item {
            flex-direction: column;
            gap: 2px;
            padding: var(--space-xs) var(--space-sm);
            font-size: 10px;
            min-width: 56px;
        }

        .nav-item.active::before {
            display: none;
        }
    }
</style>
