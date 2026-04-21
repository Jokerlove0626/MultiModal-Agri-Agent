import axios from "axios";

// 使用你现有的 baseUrl 以及服务结构即可
const api = axios.create({
	baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
	timeout: 30000,
});

export async function getGraphData(diseaseName = "", limit = 150) {
	const { data } = await api.get("/api/graph/visualize", {
		params: {
			disease_name: diseaseName,
			limit,
		},
	});
	return data;
}
