import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Fluid Magic - Custom BG", layout="wide")

st.sidebar.title("🎨 Bảng Điều Khiển")

# --- CHỨC NĂNG TẢI ẢNH TỪ BỘ SƯU TẬP ---
uploaded_file = st.sidebar.file_uploader("Chọn ảnh từ bộ sưu tập của bạn", type=["jpg", "jpeg", "png"])

# Xử lý ảnh để đưa vào code HTML
bg_image_data = ""
if uploaded_file is not None:
    # Chuyển ảnh sang dạng Base64 để nhúng trực tiếp vào HTML
    file_bytes = uploaded_file.read()
    encoded = base64.b64encode(file_bytes).decode()
    bg_image_data = f"data:image/png;base64,{encoded}"

# Các tùy chỉnh khác
p_color = st.sidebar.color_picker("Chọn màu chất lỏng:", "#FF4B4B")
is_random = st.sidebar.checkbox("Sử dụng màu cầu vồng", value=True)
p_power = st.sidebar.slider("Độ mạnh tia nước:", 5, 50, 15)

# --- NHÚNG CODE HTML/JS ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; }}
        #bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{bg_image_data}');
            background-color: #1a1a1a;
            background-size: cover; background-position: center;
            z-index: -1;
        }}
        canvas {{ display: block; cursor: crosshair; }}
    </style>
</head>
<body>
    <div id="bg"></div>
    <canvas id="canvas"></canvas>
    <script>
        // ... (Giữ nguyên logic xử lý hạt giống như code cũ mình đã đưa) ...
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        class Particle {{
            constructor(x, y, color) {{
                this.x = x; this.y = y;
                this.size = Math.random() * 10 + 2;
                this.speedX = Math.random() * 8 - 4;
                this.speedY = Math.random() * 8 - 4;
                this.color = color;
                this.gravity = 0.15;
                this.opacity = 1;
            }}
            update() {{
                this.speedY += this.gravity;
                this.x += this.speedX;
                this.y += this.speedY;
                this.opacity -= 0.015;
            }}
            draw() {{
                ctx.globalAlpha = this.opacity;
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}

        function spawn(e) {{
            const x = e.touches ? e.touches[0].clientX : e.clientX;
            const y = e.touches ? e.touches[0].clientY : e.clientY;
            for (let i = 0; i < {p_power}; i++) {{
                const color = {str(is_random).lower()} ? `hsl(${{Math.random() * 360}}, 100%, 50%)` : '{p_color}';
                particles.push(new Particle(x, y, color));
            }}
        }}
        window.addEventListener('mousedown', spawn);
        window.addEventListener('mousemove', (e) => {{ if(e.buttons === 1) spawn(e) }});
        window.addEventListener('touchmove', spawn);
        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {{
                particles[i].update();
                particles[i].draw();
                if (particles[i].opacity <= 0) {{ particles.splice(i, 1); i--; }}
            }}
            requestAnimationFrame(animate);
        }}
        animate();
    </script>
</body>
</html>
"""

components.html(html_code, height=600)

# --- CHÂN TRANG ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🚀 POWERED BY NGUYEN THANH DUY</h1>", unsafe_allow_html=True)
