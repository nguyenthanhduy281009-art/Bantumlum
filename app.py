import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. Cấu hình trang
st.set_page_config(page_title="Fluid Spray Pro - Duy", layout="wide")

# 2. Khởi tạo bộ nhớ Session State
if 'bg_base64' not in st.session_state:
    st.session_state.bg_base64 = ""

# --- SIDEBAR ---
st.sidebar.title("🔫 Fluid Spray Studio")
uploaded_file = st.sidebar.file_uploader("👤 Tải ảnh người để bắt đầu", type=["jpg", "jpeg", "png"])

# Xử lý ảnh: Chuyển sang Base64 và lưu lại để không bị mất khi chỉnh slider
if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        st.session_state.bg_base64 = base64.b64encode(file_bytes).decode()
    except Exception as e:
        st.sidebar.error("Lỗi tải ảnh, Duy thử lại nhé!")

# Thông số bắn
p_power = st.sidebar.slider("🚀 Lực bắn", 5, 40, 15)
p_size = st.sidebar.slider("💧 Cỡ giọt", 2, 20, 8)

if st.sidebar.button("🧹 RESET MÀN HÌNH"):
    st.rerun()

# --- CHUẨN BỊ DỮ LIỆU ẢNH ---
img_data = f"data:image/png;base64,{st.session_state.bg_base64}" if st.session_state.bg_base64 else ""

# --- HTML/JS: HIỆU ỨNG BẮN TRẮNG ĐỤC ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; background: #111; }}
        #bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{img_data}');
            background-size: contain; background-repeat: no-repeat; background-position: center;
            z-index: 1;
        }}
        canvas {{ position: absolute; top: 0; left: 0; z-index: 2; cursor: crosshair; }}
    </style>
</head>
<body>
    <div id="bg"></div>
    <canvas id="sprayCanvas"></canvas>

    <script>
        const canvas = document.getElementById('sprayCanvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let isMouseDown = false;

        function resize() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}

        class Particle {{
            constructor(x, y) {{
                this.x = x;
                this.y = y;
                // Bắn tỏa ra 360 độ
                const angle = Math.random() * Math.PI * 2;
                const velocity = Math.random() * {p_power};
                this.vx = Math.cos(angle) * velocity;
                this.vy = Math.sin(angle) * velocity;
                this.size = Math.random() * {p_size} + 1;
                this.gravity = 0.3;
                this.alpha = 1;
                this.decay = Math.random() * 0.015 + 0.005;
            }}

            update() {{
                this.vx *= 0.95; // Lực cản không khí
                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;
                this.alpha -= this.decay;
            }}

            draw() {{
                ctx.fillStyle = `rgba(255, 255, 245, ${{this.alpha}})`; // Màu trắng đục kem
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}

        function spawn(e) {{
            const x = e.clientX || (e.touches && e.touches[0].clientX);
            const y = e.clientY || (e.touches && e.touches[0].clientY);
            for(let i=0; i<6; i++) {{
                particles.push(new Particle(x, y));
            }}
        }}

        window.addEventListener('mousedown', (e) => {{ isMouseDown = true; spawn(e); }});
        window.addEventListener('mouseup', () => isMouseDown = false);
        window.addEventListener('mousemove', (e) => {{ if(isMouseDown) spawn(e); }});
        
        window.addEventListener('touchstart', (e) => {{ isMouseDown = true; spawn(e); }}, {{passive: false}});
        window.addEventListener('touchend', () => isMouseDown = false);
        window.addEventListener('touchmove', (e) => {{ if(isMouseDown) {{ e.preventDefault(); spawn(e); }} }}, {{passive: false}});

        function animate() {{
            // Giữ lại vết cũ nhẹ để tạo cảm giác chất lỏng dính
            ctx.fillStyle = 'rgba(0, 0, 0, 0.02)';
            // Nếu Duy muốn dính vĩnh viễn thì comment dòng dưới, nhưng sẽ rất lag
            // ctx.fillRect(0, 0, canvas.width, canvas.height); 

            for(let i=0; i<particles.length; i++) {{
                particles[i].update();
                particles[i].draw();
                if(particles[i].alpha <= 0) {{
                    particles.splice(i, 1);
                    i--;
                }}
            }}
            requestAnimationFrame(animate);
        }}

        window.addEventListener('resize', resize);
        resize();
        animate();
    </script>
</body>
</html>
"""

components.html(html_code, height=750)

# --- CHÂN TRANG ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 10px;">
        <p style="color: #555;">Duy ơi, nếu ảnh chưa hiện, hãy nhấn chọn file lại lần nữa để trình duyệt ghi nhớ nhé!</p>
        <h2 style="color: white; background: #FF4B4B; display: inline-block; padding: 10px 20px; border-radius: 10px;">🚀 POWERED BY NGUYEN THANH DUY</h2>
    </div>
""", unsafe_allow_html=True)
