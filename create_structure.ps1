$directories = @(
    "backend/shared_kernel/application/interfaces",
    "backend/shared_kernel/domain/events",
    "backend/shared_kernel/domain/exceptions",
    "backend/shared_kernel/domain/value_objects",
    "backend/shared_kernel/infrastructure/bus",
    "backend/shared_kernel/infrastructure/databases",

    "backend/modules/account_intelligence/application",
    "backend/modules/account_intelligence/domain",
    "backend/modules/account_intelligence/infrastructure",
    "backend/modules/account_intelligence/presentation",

    "backend/modules/browser/application",
    "backend/modules/browser/domain",
    "backend/modules/browser/infrastructure",
    "backend/modules/browser/presentation",

    "backend/modules/character_management/application",
    "backend/modules/character_management/domain",
    "backend/modules/character_management/infrastructure",
    "backend/modules/character_management/presentation",

    "backend/modules/decision/application",
    "backend/modules/decision/domain",
    "backend/modules/decision/infrastructure",
    "backend/modules/decision/presentation",

    "backend/modules/growth_engine/application",
    "backend/modules/growth_engine/domain",
    "backend/modules/growth_engine/infrastructure",
    "backend/modules/growth_engine/presentation",

    "backend/modules/journal/application",
    "backend/modules/journal/domain",
    "backend/modules/journal/infrastructure",
    "backend/modules/journal/presentation",

    "backend/modules/memory/application",
    "backend/modules/memory/domain",
    "backend/modules/memory/infrastructure",
    "backend/modules/memory/presentation",

    "backend/modules/orchestrator/application",
    "backend/modules/orchestrator/domain",
    "backend/modules/orchestrator/infrastructure",
    "backend/modules/orchestrator/presentation",

    "backend/modules/research/application",
    "backend/modules/research/domain",
    "backend/modules/research/infrastructure",
    "backend/modules/research/presentation",

    "backend/modules/task_manager/application",
    "backend/modules/task_manager/domain",
    "backend/modules/task_manager/infrastructure",
    "backend/modules/task_manager/presentation",

    "backend/modules/platform_agents/x/adapters",
    "backend/modules/platform_agents/x/application",
    "backend/modules/platform_agents/x/presentation",

    "backend/modules/platform_agents/instagram/adapters",
    "backend/modules/platform_agents/instagram/application",
    "backend/modules/platform_agents/instagram/presentation",

    "backend/modules/platform_agents/tiktok/adapters",
    "backend/modules/platform_agents/tiktok/application",
    "backend/modules/platform_agents/tiktok/presentation",

    "backend/tests/e2e",
    "backend/tests/integration",
    "backend/tests/unit"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

New-Item -ItemType File -Force -Path "backend\__init__.py" | Out-Null

Get-ChildItem -Path "backend" -Recurse -Directory | ForEach-Object {
    New-Item -ItemType File -Force -Path "$($_.FullName)\__init__.py" | Out-Null
}

Write-Host ""
Write-Host "========================================"
Write-Host "Project Athena Backend Created Successfully!"
Write-Host "========================================"