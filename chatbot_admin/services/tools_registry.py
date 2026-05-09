class ToolsRegistry:
    ADMIN_TOOLS_REGISTRY = {
        "get_platform_stats": {
            "name": "get_platform_stats",
            "description": "Get overall platform statistics (doctors, patients, appointments)",
            "category": "stats",
            "endpoint": "/api/admin/stats/",
            "method": "GET",
            "parameters": {}
        },
        "list_pending_doctors": {
            "name": "list_pending_doctors",
            "description": "List doctors waiting for verification",
            "category": "management",
            "endpoint": "/api/admin/pending-doctors/",
            "method": "GET",
            "parameters": {}
        },
        "get_system_health": {
            "name": "get_system_health",
            "description": "Check the status of system services",
            "category": "system",
            "endpoint": "/api/admin/health/",
            "method": "GET",
            "parameters": {}
        }
    }

    @staticmethod
    def get_all_tools():
        return ToolsRegistry.ADMIN_TOOLS_REGISTRY

    @staticmethod
    def get_categories():
        categories = set()
        for tool in ToolsRegistry.ADMIN_TOOLS_REGISTRY.values():
            categories.add(tool["category"])
        return list(categories)
