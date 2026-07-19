<script lang="ts">
    import StatusBadge from '../components/StatusBadge.svelte';
    import { Users } from '@lucide/svelte';

    const accessRoles = [
        { role: 'Admin', users: 2, scope: 'All machines', note: 'Full control and approvals', color: 'brand' as const },
        { role: 'Engineer', users: 7, scope: 'Assigned cells', note: 'Upload and view programs', color: 'success' as const },
        { role: 'Viewer', users: 3, scope: 'Read only', note: 'Compliance and reporting', color: 'neutral' as const },
    ];
</script>

<div class="access-page">
    <div class="card">
        <div class="card-header">
            <h3>Access Control</h3>
            <span class="card-action">Role coverage</span>
        </div>

        <div class="role-grid">
            {#each accessRoles as role}
                <div class="role-card">
                    <div class="role-header">
                        <span class="role-name">{role.role}</span>
                        <StatusBadge variant={role.color}>{role.users} users</StatusBadge>
                    </div>
                    <p class="role-scope">{role.scope}</p>
                    <p class="role-note">{role.note}</p>
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    .access-page { max-width: 800px; }

    .card {
        background: var(--color-surface-1);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
    }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-lg); }
    .card-header h3 { font-size: 18px; font-weight: 600; color: var(--color-ink); margin: 0; }
    .card-action { font-size: 12px; font-weight: 600; color: var(--color-ink-subtle); }

    .role-grid {
        display: grid;
        gap: var(--space-md);
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    }

    .role-card {
        background: var(--color-surface-2);
        border: 1px solid var(--color-hairline);
        border-radius: var(--radius-lg);
        padding: var(--space-md);
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .role-header { display: flex; justify-content: space-between; align-items: center; }
    .role-name { font-size: 16px; font-weight: 600; color: var(--color-ink); }
    .role-scope { font-size: 13px; color: var(--color-ink-subtle); margin: 0; }
    .role-note { font-size: 12px; color: var(--color-ink-tertiary); margin: 0; }
</style>
