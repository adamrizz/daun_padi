const upload = document.getElementById("upload");
const preview = document.getElementById("preview");
const result = document.getElementById("result");

upload.addEventListener("change", async () => {
  const file = upload.files[0];
  preview.src = URL.createObjectURL(file);

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("https://yolo-backend-production.up.railway.app/", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  result.textContent = JSON.stringify(data, null, 2);
});
