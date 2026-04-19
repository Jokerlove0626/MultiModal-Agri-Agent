import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/home.vue";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{ path: "/", name: "home", component: Home },
		{
			path: "/chat",
			name: "chat",
			component: () => import("../views/chat.vue"),
		},
		{
			path: "/graph",
			name: "graph",
			component: () => import("../views/graph.vue"),
		},
		{
			path: "/monitor",
			name: "monitor",
			component: () => import("../views/monitor.vue"),
		},
		{
			path: "/knowledge",
			name: "knowledge",
			component: () => import("../views/knowledge.vue"),
		},
	],
});

export default router;
