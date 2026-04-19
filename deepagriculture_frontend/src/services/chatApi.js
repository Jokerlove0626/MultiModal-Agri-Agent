const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

export function getApiBaseUrl() {
	const envValue = import.meta.env?.VITE_API_BASE_URL;
	if (typeof envValue === "string" && envValue.trim()) return envValue.trim();
	return DEFAULT_API_BASE_URL;
}

function joinUrl(baseUrl, path) {
	const trimmedBaseUrl = String(baseUrl).replace(/\/+$/, "");
	const trimmedPath = String(path).startsWith("/") ? path : `/${path}`;
	return `${trimmedBaseUrl}${trimmedPath}`;
}

export async function postChat({ query, sessionId, province, city } = {}) {
	const baseUrl = getApiBaseUrl();
	const url = joinUrl(baseUrl, "/api/chat/");

	const resp = await fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			query,
			session_id: sessionId || undefined,
			province: province || undefined,
			city: city || undefined,
		}),
	});

	const data = await resp.json().catch(() => null);
	if (!resp.ok) {
		const message = data?.detail || data?.message || resp.statusText;
		throw new Error(message);
	}
	return data;
}

export async function postChatStream({
	query,
	sessionId,
	onChunk,
	signal,
} = {}) {
	const baseUrl = getApiBaseUrl();
	const url = joinUrl(baseUrl, "/api/chat/stream");

	const resp = await fetch(url, {
		method: "POST",
		signal,
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			query,
			session_id: sessionId || undefined,
		}),
	});

	if (!resp.ok) {
		const data = await resp.json().catch(() => null);
		const message = data?.detail || data?.message || resp.statusText;
		throw new Error(message);
	}
	if (!resp.body) throw new Error("流式响应不可用（response.body 为空）");

	const reader = resp.body.getReader();
	const decoder = new TextDecoder("utf-8");
	let buffer = "";
	let fullText = "";

	const flushEvent = (eventText) => {
		const blocks = String(eventText).split("\n");
		for (const block of blocks) {
			if (!block.startsWith("data: ")) continue;
			const text = block.slice("data: ".length);
			if (text === "[DONE]") return { done: true };
			if (text) {
				fullText += text;
				if (typeof onChunk === "function") onChunk(text, fullText);
			}
		}
		return { done: false };
	};

	while (true) {
		const { done, value } = await reader.read();
		if (done) break;
		buffer += decoder.decode(value, { stream: true });

		let sepIndex;
		while ((sepIndex = buffer.indexOf("\n\n")) !== -1) {
			const eventText = buffer.slice(0, sepIndex);
			buffer = buffer.slice(sepIndex + 2);
			const { done: isDone } = flushEvent(eventText);
			if (isDone) return fullText;
		}
	}

	if (buffer.trim()) flushEvent(buffer);
	return fullText;
}

export async function postIdentify({
	file,
	cropName,
	userText,
	sessionId,
} = {}) {
	const baseUrl = getApiBaseUrl();
	const url = joinUrl(baseUrl, "/api/chat/identify");

	const formData = new FormData();
	formData.append("file", file);
	if (cropName !== undefined && cropName !== null)
		formData.append("crop_name", cropName);
	if (userText !== undefined && userText !== null)
		formData.append("user_text", userText);
	if (sessionId !== undefined && sessionId !== null)
		formData.append("session_id", sessionId);

	const resp = await fetch(url, {
		method: "POST",
		body: formData,
	});

	const data = await resp.json().catch(() => null);
	if (!resp.ok) {
		const message = data?.detail || data?.message || resp.statusText;
		throw new Error(message);
	}
	return data;
}
