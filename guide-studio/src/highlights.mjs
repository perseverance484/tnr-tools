export async function prepareHighlight(file) {
  if (!["image/png", "image/jpeg", "image/webp"].includes(file.type))
    throw Error("Choose a PNG, JPEG, or WebP screenshot.");
  if (file.size > 10_000_000)
    throw Error("The source screenshot must be under 10 MB.");
  const bitmap = await createImageBitmap(file);
  try {
    let scale = Math.min(1, 1600 / Math.max(bitmap.width, bitmap.height));
    for (let attempt = 0; attempt < 5; attempt++) {
      const canvas = document.createElement("canvas");
      canvas.width = Math.max(1, Math.floor(bitmap.width * scale));
      canvas.height = Math.max(1, Math.floor(bitmap.height * scale));
      const ctx = canvas.getContext("2d");
      ctx.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
      const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/webp", 0.8 - attempt * 0.08),
      );
      if (blob?.type === "image/webp" && blob.size <= 350_000)
        return await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(String(reader.result));
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });
      scale *= 0.8;
    }
    throw Error(
      "This image could not be compressed. Choose a smaller screenshot.",
    );
  } finally {
    bitmap.close();
  }
}
