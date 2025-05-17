import React, { useState } from "react";
import "./App.css";

function App() {
  const [teacherId, setTeacherId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [newTeacher, setNewTeacher] = useState("");
  const [addTeacherMsg, setAddTeacherMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError("");
    if (!teacherId) {
      setError("Por favor ingresa un ID de profesor.");
      return;
    }
    try {
      const res = await fetch(
        `http://localhost:8000/schedules/validate-schedule/${teacherId}`
      );
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail ? data.detail.join(", ") : "Error al validar horario");
        return;
      }
      setResult(data);
    } catch (err) {
      setError("No se pudo conectar con el servidor");
    }
  };
  const [teachers, setTeachers] = useState([]);

    // En tu JSX, antes del formulario de validación:
    {teachers.length > 0 && (
      <div style={{ marginBottom: 20 }}>
        <strong>Profesores registrados:</strong>
        <ul>
          {teachers.map(t => (
            <li key={t.Teacher_ID}>
              {t.Teacher_ID}: {t.Name}
            </li>
          ))}
        </ul>
      </div>
    )}

  // NUEVO: Función para agregar profesor
  const handleAddTeacher = async (e) => {
    e.preventDefault();
    setAddTeacherMsg("");
    if (!newTeacher) return;
    try {
      const res = await fetch("http://localhost:8000/teachers/", {
        
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ Name: newTeacher }),
      });
      if (res.ok) {
        setAddTeacherMsg("Profesor agregado correctamente.");
        setNewTeacher("");
      } else {
        const data = await res.json();
        setAddTeacherMsg(data.detail || "Error al agregar profesor.");
      }
    } catch {
      setAddTeacherMsg("No se pudo conectar con el servidor.");
    }
  };







  return (
    <div className="App">
      <header className="App-header">
        <h2>Validador de Horario de Profesor</h2>

        {/* Formulario para agregar profesor */}
        <form onSubmit={handleAddTeacher} style={{ marginBottom: 20 }}>
          <input
            type="text"
            placeholder="Nombre del profesor"
            value={newTeacher}
            onChange={(e) => setNewTeacher(e.target.value)}
            style={{ padding: 8, marginRight: 8 }}
            required
          />
          <button type="submit" style={{ padding: 8 }}>Agregar Profesor</button>
        </form>
        {addTeacherMsg && <div style={{ color: "#0f0", marginBottom: 10 }}>{addTeacherMsg}</div>}

        {/* Formulario para validar horario */}
        <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
          <input
            type="number"
            placeholder="ID del profesor"
            value={teacherId}
            onChange={(e) => setTeacherId(e.target.value)}
            style={{ padding: 8, marginRight: 8 }}
            required
          />
          <button type="submit" style={{ padding: 8 }}>Validar</button>
        </form>
        {error && <div style={{ color: "red", marginBottom: 10 }}>{error}</div>}
        {result && (
          <div style={{ background: "#222", padding: 16, borderRadius: 8 }}>
            <strong>{result.message}</strong>
            {result.conflicts && result.conflicts.length > 0 && (
              <ul style={{ textAlign: "left" }}>
                {result.conflicts.map((conflict, idx) => (
                  <li key={idx}>{conflict}</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;