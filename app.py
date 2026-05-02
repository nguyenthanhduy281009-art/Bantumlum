import streamlit as st
import streamlit.components.v1 as components
import base64
import json

# Cấu hình giao diện
st.set_page_config(page_title="Paint Master Pro - Duy", layout="wide")

# --- KHỞI TẠO BỘ NHỚ TẠM (SESSION STATE) ---
if 'painted_points' not in st.session_state:
    st.session_state.painted_points = []
if 'bg_data' not in st.session_state:
    st.session_state.bg_data = ""

# --- SIDEBAR ---
st.sidebar.title("🎮 Paint Studio")
uploaded_file = st.sidebar.file_uploader("🖼️ Tải ảnh nền", type=["jpg", "jpeg", "png"])

# Kiểm tra nếu người dùng vừa tải ảnh mới lên
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    # Lưu vào session_state để không bị mất khi chỉnh slider
    st.session_state.bg_data = f"data:image/png;base64,{base64.b64encode(file_bytes).decode()}"

# Lấy dữ liệu ảnh từ bộ nhớ tạm
bg_data = st.session_state.bg_data

p_color = st.sidebar.color_picker("🎨 Màu sơn", "#00F2FF")
is_rainbow = st.sidebar.checkbox("🌈 Chế độ cầu vồng", value=True)
p_size = st.sidebar.slider("💧 Kích thước giọt", 5, 30, 15)
p_power = st.sidebar.slider("🔫 Áp lực phun", 10, 100, 30)

# Nút Reset xóa sạch cả vết sơn và ảnh nền (nếu muốn)
if st.sidebar.button("🧹 RESET MÀN HÌNH"):
    st.session_state.painted_points = []
    # st.session_state.bg_data = "" # Bỏ comment dòng này nếu muốn xóa luôn ảnh khi Reset
    st.rerun()

# Chuyển danh sách điểm sang JSON
points_json = json.dumps(st.session_state.painted_points)

# --- CODE HTML/JS ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; background: #1a1a1a; }}
        #bg {{ 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background-image: url('{bg_data}'); 
            background-size: cover; 
            background-position: center; 
            z-index: -1; 
        }}
        canvas {{ position: absolute; top: 0; left: 0; }}
    </style>
</head>
<body>
    <div id="bg"></div>
    <canvas id="paintCanvas"></canvas>
    <canvas id="fluidCanvas"></canvas>

    <script>
        const pCanvas = document.getElementById('paintCanvas');
        const fCanvas = document.getElementById('fluidCanvas');
        const pCtx = pCanvas.getContext('2d');
        const fCtx = fCanvas.getContext('2d');
        
        let width, height;
        let particles = [];
        let savedPoints = {points_json};

        function resize() {{
            width = window.innerWidth;
            height = window.innerHeight;
            pCanvas.width = fCanvas.width = width;
            pCanvas.height = fCanvas.height = height;
            redrawSavedPoints();
        }}

        function redrawSavedPoints() {{
            if (!savedPoints) return;
            savedPoints.forEach(p => {{
                pCtx.globalAlpha = 0.8;
                pCtx.fillStyle = p.color;
                pCtx.filter = 'blur(1px)';
                pCtx.beginPath();
                pCtx.arc(p.x, p.y, p.size * 1.5, 0, Math.PI * 2);
                pCtx.fill();
            }});
        }}

        // Giữ nguyên logic Drop và emit như cũ ...
        class Drop {{
            constructor(x, y, color, size) {{
                this.x = x; this.y = y;
                this.size = size * (Math.random() * 0.5 + 0.5);
                this.color = color;
                const angle = Math.random() * Math.PI * 2;
                const force = Math.random() * {p_power / 5};
                this.vx = Math.cos(angle) * force;
                this.vy = Math.sin(angle) * force;
                this.gravity = 0.2; this.life = 1;
            }}
            update() {{
                this.vy += this.gravity;
                this.x += this.vx; this.y += this.vy;
                this.life -= 0.02;
                if (this.life < 0.1) {{ this.stick(); return false; }}
                return true;
            }}
            stick() {{
                pCtx.globalAlpha = 0.8;
                pCtx.fillStyle = this.color;
                pCtx.filter = 'blur(1px)';
                pCtx.beginPath();
                pCtx.arc(this.x, this.y, this.size * 1.5, 0, Math.PI * 2);
                pCtx.fill();
            }}
            draw() {{
                fCtx.globalAlpha = this.life;
                fCtx.fillStyle = this.color;
                fCtx.beginPath();
                fCtx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                fCtx.fill();
            }}
        }}

        function emit(e) {{
            const x = e.touches ? e.touches[0].clientX : e.clientX;
            const y = e.touches ? e.touches[0].clientY : e.clientY;
            const color = {str(is_rainbow).lower()} ? `hsl(${{Math.random() * 360}}, 80%, 60%)` : '{p_color}';
            for(let i=0; i<5; i++) particles.push(new Drop(x, y, color, {p_size}));
        }}

        window.addEventListener('mousedown', emit);
        window.addEventListener('mousemove', (e) => {{ if(e.buttons === 1) emit(e); }});
        window.addEventListener('touchmove', emit);
        window.addEventListener('resize', resize);
        resize();

        function frame() {{
            fCtx.clearRect(0, 0, width, height);
            for(let i=0; i<particles.length; i++) {{
                if(!particles[i].update()) {{ particles.splice(i, 1); i--; }}
                else particles[i].draw();
            }}
            requestAnimationFrame(frame);
        }}
        frame();
    </script>
</body>
</html>
"""

components.html(html_code, height=700)

# --- CHÂN TRANG ---
st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 15px; background: #1e1e1e; border: 2px solid #FF4B4B; box-shadow: 0 0 15px #FF4B4B; margin-top: 20px;">
        <h2 style="color: #FF4B4B; margin: 0; font-family: sans-serif;">🚀 POWERED BY</h2>
        <h1 style="color: #FFFFFF; margin: 5px 0; font-size: 40px; text-shadow: 0 0 10px #FF4B4B;">NGUYEN THANH DUY</h1>
    </div>
    """, unsafe_allow_html=True)
