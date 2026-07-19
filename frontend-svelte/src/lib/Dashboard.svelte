<script lang="ts">
    import { user } from './authStore';
    import { theme } from './design/themeStore';

    // Layout components
    import Sidebar from './components/Sidebar.svelte';
    import TopBar from './components/TopBar.svelte';
    import CommandPalette from './components/CommandPalette.svelte';
    import Toast from './components/Toast.svelte';
    import { addToast } from './stores/toastStore';
    import Modal from './components/Modal.svelte';
    import { LogOut } from '@lucide/svelte';

    // Page components
    import OverviewPage from './pages/OverviewPage.svelte';
    import UploadPage from './pages/UploadPage.svelte';
    import FilesPage from './pages/FilesPage.svelte';
    import RollbackPage from './pages/RollbackPage.svelte';
    import ComparePage from './pages/ComparePage.svelte';
    import MachinesPage from './pages/MachinesPage.svelte';
    import AnalyticsPage from './pages/AnalyticsPage.svelte';
    import AuditTrailPage from './pages/AuditTrailPage.svelte';
    import AccessControlPage from './pages/AccessControlPage.svelte';
    import SettingsPage from './pages/SettingsPage.svelte';

    let activeTab = 'overview';
    let commandPaletteOpen = false;
    let showLogoutModal = false;

    const tabTitles: Record<string, string> = {
        overview: 'Executive Overview',
        upload: 'Upload Program',
        view: 'File Browser',
        rollback: 'Version Rollback',
        compare: 'Version Compare',
        machines: 'Machine Fleet',
        analytics: 'Analytics & Reports',
        audit: 'Audit Trail',
        access: 'Access Control',
        settings: 'Settings',
    };

    function handleTabChange(tab: string) {
        activeTab = tab;
    }

    function handleCommandPalette() {
        commandPaletteOpen = true;
    }

    function handleCommandAction(event: any) {
        const action = event;
        if (action?.id) {
            activeTab = action.id;
        }
    }

    function confirmLogout() {
        showLogoutModal = true;
    }

    function cancelLogout() {
        showLogoutModal = false;
    }

    function proceedLogout() {
        showLogoutModal = false;
        user.set(null);
    }

    // Global keyboard shortcuts
    function handleGlobalKeydown(e: KeyboardEvent) {
        // Ctrl+K / Cmd+K → Command Palette
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            commandPaletteOpen = !commandPaletteOpen;
        }
    }
</script>

<svelte:head>
    <title>AutoVault — {tabTitles[activeTab] || 'Dashboard'}</title>
</svelte:head>

<svelte:window on:keydown={handleGlobalKeydown} />

<div class="app-shell">
    <Sidebar
        {activeTab}
        onTabChange={handleTabChange}
        onLogout={confirmLogout}
    />

    <main class="main-area">
        <TopBar
            pageTitle={tabTitles[activeTab] || activeTab}
            onCommandPalette={handleCommandPalette}
        />

        <div class="page-content">
            <div class="page-scroll">
                {#if activeTab === 'overview'}
                    <OverviewPage onNavigate={handleTabChange} />
                {:else if activeTab === 'upload'}
                    <UploadPage showToast={addToast} />
                {:else if activeTab === 'view'}
                    <FilesPage showToast={addToast} />
                {:else if activeTab === 'rollback'}
                    <RollbackPage showToast={addToast} />
                {:else if activeTab === 'compare'}
                    <ComparePage showToast={addToast} />
                {:else if activeTab === 'machines'}
                    <MachinesPage showToast={addToast} />
                {:else if activeTab === 'analytics'}
                    <AnalyticsPage />
                {:else if activeTab === 'audit'}
                    <AuditTrailPage />
                {:else if activeTab === 'access'}
                    <AccessControlPage />
                {:else if activeTab === 'settings'}
                    <SettingsPage showToast={addToast} />
                {/if}
            </div>
        </div>
    </main>
</div>

<!-- Command Palette -->
<CommandPalette
    open={commandPaletteOpen}
    onClose={() => commandPaletteOpen = false}
    onAction={handleCommandAction}
/>

<!-- Toast Container -->
<Toast />

<!-- Logout Modal -->
<Modal open={showLogoutModal} title="Confirm Logout" size="sm" onClose={cancelLogout}>
    <p class="confirm-text">Are you sure you want to log out? Any unsaved changes will be lost.</p>
    <div slot="footer">
        <button class="secondary-btn" on:click={cancelLogout}>Cancel</button>
        <button class="danger-btn" on:click={proceedLogout}>
            <LogOut size={14} /> Logout
        </button>
    </div>
</Modal>

<style>
    .app-shell {
        display: flex;
        min-height: 100vh;
        background: var(--color-canvas);
    }

    .main-area {
        margin-left: var(--sidebar-width);
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0;
        min-height: 100vh;
        transition: margin-left var(--transition-slow);
    }

    .page-content {
        flex: 1;
        display: flex;
        min-height: 0;
    }

    .page-scroll {
        flex: 1;
        padding: var(--space-lg);
        overflow-y: auto;
    }

    .confirm-text {
        font-size: 15px;
        color: var(--color-ink-muted);
        line-height: 1.6;
    }

    .secondary-btn {
        padding: 8px 16px;
        border: 1px solid var(--color-hairline);
        background: transparent;
        color: var(--color-ink-subtle);
        font-size: 14px;
        font-weight: 500;
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all var(--transition-fast);
    }

    .secondary-btn:hover {
        background: var(--color-surface-2);
        color: var(--color-ink);
    }

    .danger-btn {
        padding: 8px 16px;
        background: var(--color-error);
        color: #ffffff;
        border: none;
        font-size: 14px;
        font-weight: 500;
        border-radius: var(--radius-md);
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: var(--space-xs);
        transition: background var(--transition-fast);
    }

    .danger-btn:hover {
        background: #dc2626;
    }

    @media (max-width: 1024px) {
        .main-area {
            margin-left: var(--sidebar-collapsed);
        }
    }

    @media (max-width: 768px) {
        .main-area {
            margin-left: 0;
            margin-bottom: 56px;
        }

        .page-scroll {
            padding: var(--space-md);
        }
    }
</style>
