<script lang="ts">
    import { user } from '../authStore';
    import {
        LayoutDashboard, Upload, List, RotateCcw, ArrowLeftRight,
        LogOut, User, Settings, BarChart3, Users, Shield,
        ChevronLeft, Activity
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
    <!-- Header with Brand & Collapse Toggle at the Top Right -->
    <div class="sidebar-header">
        <div class="brand-left">
            <img src="/assets/logo-av-2.png" alt="AutoVault" class="sidebar-logo" />
            {#if !collapsed}
                <span class="sidebar-brand">AutoVault</span>
            {/if}
        </div>
        <button
            class="collapse-toggle-top"
            on:click={() => collapsed = !collapsed}
            title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            aria-label="Toggle Sidebar"
        >
            <ChevronLeft size={16} class={collapsed ? 'rotated' : ''} />
        </button>
    </div>

    <!-- Nav Items - Strict Left Alignment -->
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

    <!-- Footer User Pill & Logout -->
    <div class="sidebar-footer">
        <div class="user-pill" title="Logged in as {$user?.name}">
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
            <LogOut size={16} />
            {#if !collapsed}
                <span>Logout</span>
            {/if}
        </button>
    </div>
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
        justify-content: space-between;
        padding: var(--space-md);
        min-height: var(--topbar-height);
        border-bottom: 1px solid var(--color-hairline);
    }

    .brand-left {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
    }

    .sidebar-logo {
        height: 24px;
        width: auto;
        flex-shrink: 0;
    }

    .sidebar-brand {
        font-family: var(--font-display);
        font-size: 16px;
        font-weight: 700;
        letter-spacing: -0.4px;
        color: var(--color-ink);
        white-space: nowrap;
    }

    .collapse-toggle-top {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-md);
        color: var(--color-ink-subtle);
        cursor: pointer;
        transition: all var(--transition-fast);
        flex-shrink: 0;
    }

    .collapse-toggle-top:hover {
        background: var(--color-surface-3);
        color: var(--color-ink);
        border-color: var(--color-hairline-strong);
    }

    .collapse-toggle-top :global(.rotated) {
        transform: rotate(180deg);
    }

    .sidebar-nav {
        flex: 1;
        padding: var(--space-xs);
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        width: 100%;
        padding: 9px var(--space-sm);
        border: none;
        background: transparent;
        color: var(--color-ink-subtle);
        font-size: 14px;
        font-weight: 500;
        text-align: left;
        justify-content: flex-start;
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
        top: 4px;
        bottom: 4px;
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
        text-align: left;
    }

    .sidebar-footer {
        padding: var(--space-xs) var(--space-sm);
        border-top: 1px solid var(--color-hairline);
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .user-pill {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        padding: var(--space-xs);
        background: var(--color-surface-2);
        border-radius: var(--radius-md);
        justify-content: flex-start;
    }

    .user-avatar {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 26px;
        height: 26px;
        background: var(--color-primary);
        color: var(--color-on-primary);
        border-radius: var(--radius-full);
        flex-shrink: 0;
    }

    .user-info {
        display: flex;
        flex-direction: column;
        min-width: 0;
        text-align: left;
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
        font-size: 10px;
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

    @media (max-width: 1024px) {
        .sidebar {
            width: var(--sidebar-collapsed);
        }
        .sidebar-brand, .nav-label, .user-info, .logout-btn span {
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
        .sidebar-footer {
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
