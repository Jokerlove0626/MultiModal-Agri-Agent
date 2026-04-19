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

	try {
		while (true) {
			const { done, value } = await reader.read();
			if (done) break;

			// 解码二进制数据为文本
			const chunk = decoder.decode(value, { stream: true });
			buffer += chunk;

			// 按SSE协议分割数据包（标准格式：data: ...\n\n）
			const lines = buffer.split("\n\n");
			buffer = lines.pop() || ""; // 保留不完整的行到下一次处理

			// 遍历处理每一个完整数据包
			for (const line of lines) {
				if (!line.trim() || line.startsWith(":")) continue;

				// 提取内容
				// 注意：这里由于后端是纯文本，如果有空格需要保留，所以直接截取。
				let dataStr = line.replace(/^data:\s*/, "");

				// 流结束标记
				if (dataStr.trim() === "[DONE]") {
					reader.cancel();
					return fullText;
				}

				// 累加真正的流式回答并回调渲染
				if (dataStr) {
					fullText += dataStr;
					if (typeof onChunk === "function")
						onChunk(dataStr, fullText);
				}
			}
		}
	} catch (e) {
		if (e.name === "AbortError") {
			console.log("Stream aborted manually");
		} else {
			throw e;
		}
	}

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
