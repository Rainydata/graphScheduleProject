import React, { useState, useEffect } from "react";
import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";
import "./App.css";

const TABS = [
  { key: "teachers", label: "Profesores" },
  { key: "classrooms", label: "Aulas" },
  { key: "courses", label: "Materias" },
  { key: "assign", label: "Asignar Horario" },
  { key: "block", label: "Bloquear Horario" },
  { key: "validate", label: "Validar Horario" },
  { key: "calendar", label: "Ver Calendario" },
  { key: "graph", label: "Grafo de Conflictos" },
];

function App() {
  const [activeTab, setActiveTab] = useState("teachers");

  // Estados para profesores
  const [teachers, setTeachers] = useState([]);
  const [newTeacher, setNewTeacher] = useState("");
  const [addTeacherMsg, setAddTeacherMsg] = useState("");

  // Estados para aulas
  const [classrooms, setClassrooms] = useState([]);
  const [newClassroom, setNewClassroom] = useState({
    Name_Classroom: "",
    Code_Classroom: "",
    System_room: false
  });
  const [addClassroomMsg, setAddClassroomMsg] = useState("");

  // Estados para cursos
  const [courses, setCourses] = useState([]);
  const [newCourse, setNewCourse] = useState({
    code_academic_space: "",
    name: "",
    franja: "",
    grupo: "",
    weekly_hours: "",
    Teacher_ID: "",
    Classroom_ID: "",
    system_room: false
  });
  const [addCourseMsg, setAddCourseMsg] = useState("");

  // Estado para validación de horario
  const [teacherId, setTeacherId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // Estados para asignar horario
  const [assignCourseId, setAssignCourseId] = useState("");
  const [assignDay, setAssignDay] = useState("");
  const [assignBlock, setAssignBlock] = useState("");
  const [assignMsg, setAssignMsg] = useState("");

  // Estados para bloquear horario a profesor
  const [blockTeacherId, setBlockTeacherId] = useState("");
  const [blockDay, setBlockDay] = useState("");
  const [blockBlock, setBlockBlock] = useState("");
  const [blockMsg, setBlockMsg] = useState("");

  // Estado para los bloqueos actuales del profesor seleccionado
  const [currentBlocks, setCurrentBlocks] = useState([]);
  const [loadingBlocks, setLoadingBlocks] = useState(false);

  // Estado para todos los horarios (para la pestaña calendario y grafo)
  const [allSchedules, setAllSchedules] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/teachers/")
      .then(res => res.json())
      .then(data => setTeachers(data));
    fetch("http://localhost:8000/classrooms/")
      .then(res => res.json())
      .then(data => setClassrooms(data));
    fetch("http://localhost:8000/courses/")
      .then(res => res.json())
      .then(data => setCourses(data));
  }, [addTeacherMsg, addClassroomMsg, addCourseMsg, assignMsg, blockMsg]);

  // Cargar bloqueos cuando se selecciona un profesor
  useEffect(() => {
    if (!blockTeacherId) {
      setCurrentBlocks([]);
      return;
    }
    setLoadingBlocks(true);
    fetch(`http://localhost:8000/teachers/${blockTeacherId}/blocked/`)
      .then(res => res.json())
      .then(data => {
        setCurrentBlocks(data);
        setLoadingBlocks(false);
      })
      .catch(() => {
        setCurrentBlocks([]);
        setLoadingBlocks(false);
      });
  }, [blockTeacherId, blockMsg]);

  // Cargar todos los horarios cuando se selecciona la pestaña calendario o grafo
  // Cargar todos los horarios cuando se selecciona la pestaña calendario o grafo
  useEffect(() => {
    if (activeTab === "calendar") {
      fetch("http://localhost:8000/schedules/all/")
        .then(res => res.json())
        .then(data => setAllSchedules(data));
    } else if (activeTab === "graph") {
      fetch("http://localhost:8000/schedules/graph-data/")
        .then(res => res.json())
        .then(data => setAllSchedules(data));
    }
  }, [activeTab, assignMsg]);

  // Agregar profesor
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

  // Agregar aula
  const handleAddClassroom = async (e) => {
    e.preventDefault();
    setAddClassroomMsg("");
    if (!newClassroom.Name_Classroom || !newClassroom.Code_Classroom) {
      setAddClassroomMsg("Completa todos los campos.");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/classrooms/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          Name_Classroom: newClassroom.Name_Classroom,
          Code_Classroom: newClassroom.Code_Classroom,
          System_room: newClassroom.System_room,
        }),
      });
      if (res.ok) {
        setAddClassroomMsg("Aula agregada correctamente.");
        setNewClassroom({ Name_Classroom: "", Code_Classroom: "", System_room: false });
      } else {
        const data = await res.json();
        setAddClassroomMsg(data.detail || "Error al agregar aula.");
      }
    } catch {
      setAddClassroomMsg("No se pudo conectar con el servidor.");
    }
  };

  // Agregar curso
  const handleAddCourse = async (e) => {
    e.preventDefault();
    setAddCourseMsg("");
    if (
      newCourse.code_academic_space === "" ||
      newCourse.name === "" ||
      newCourse.franja === "" ||
      newCourse.grupo === "" ||
      newCourse.weekly_hours === "" ||
      newCourse.Teacher_ID === "" ||
      newCourse.Classroom_ID === ""
    ) {
      setAddCourseMsg("Completa todos los campos de curso.");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/courses/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code_academic_space: Number(newCourse.code_academic_space),
          name: newCourse.name,
          franja: newCourse.franja,
          grupo: newCourse.grupo,
          weekly_hours: Number(newCourse.weekly_hours),
          Teacher_ID: Number(newCourse.Teacher_ID),
          Classroom_ID: Number(newCourse.Classroom_ID),
          system_room: newCourse.system_room,
        }),
      });
      if (res.ok) {
        setAddCourseMsg("Materia agregada correctamente.");
        setNewCourse({
          code_academic_space: "",
          name: "",
          franja: "",
          grupo: "",
          weekly_hours: "",
          Teacher_ID: "",
          Classroom_ID: "",
          system_room: false,
        });
      } else {
        const data = await res.json();
        setAddCourseMsg(data.detail || "Error al agregar materia.");
      }
    } catch (error) {
      setAddCourseMsg("No se pudo conectar con el servidor.");
    }
  };

  // Asignar horario a materia
  const handleAssignSchedule = async (e) => {
    e.preventDefault();
    setAssignMsg("");
    if (!assignCourseId || !assignDay || !assignBlock) {
      setAssignMsg("Completa todos los campos.");
      return;
    }
    const [start_time, end_time] = assignBlock.split("-");
    try {
      const res = await fetch("http://localhost:8000/schedules/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          Course_ID: assignCourseId,
          day: assignDay,
          start_time,
          end_time
        }),
      });
      const data = await res.json();
      if (res.ok) {
        if (data.conflicto) {
          setAssignMsg("Horario asignado, pero tiene conflicto: " + data.conflicto);
        } else {
          setAssignMsg("Horario asignado correctamente.");
        }
        const assignedCourse = courses.find(c => c.course_ID === Number(assignCourseId));
        if (assignedCourse && assignedCourse.Teacher_ID) {
          const valRes = await fetch(
            `http://localhost:8000/schedules/validate-schedule/${assignedCourse.Teacher_ID}`
          );
          const valData = await valRes.json();
          setResult(valData);
          setTeacherId(String(assignedCourse.Teacher_ID));
        }
      } else {
        if (Array.isArray(data.detail)) {
          setAssignMsg(data.detail.map(e => e.msg).join(" | "));
        } else if (data.detail) {
          setAssignMsg(data.detail);
        } else {
          setAssignMsg("Error al asignar horario.");
        }
      }
    } catch {
      setAssignMsg("No se pudo conectar con el servidor.");
    }
  };

  // Bloquear horario a profesor
  const handleBlockSchedule = async (e) => {
    e.preventDefault();
    setBlockMsg("");
    if (!blockTeacherId || !blockDay || !blockBlock) {
      setBlockMsg("Completa todos los campos.");
      return;
    }
    const [start_time, end_time] = blockBlock.split("-");
    try {
      const res = await fetch("http://localhost:8000/teachers/block-schedule/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          teacher_id: blockTeacherId,
          day: blockDay,
          start_time,
          end_time
        }),
      });
      if (res.ok) {
        setBlockMsg("Horario bloqueado correctamente.");
      } else {
        const data = await res.json();
        if (Array.isArray(data.detail)) {
          setBlockMsg(data.detail.map(e => e.msg).join(" | "));
        } else if (data.detail) {
          setBlockMsg(data.detail);
        } else {
          setBlockMsg("Error al bloquear horario.");
        }
      }
    } catch {
      setBlockMsg("No se pudo conectar con el servidor.");
    }
  };

  // Desbloquear un horario
  const handleUnblock = async (block) => {
    setBlockMsg("");
    try {
      const res = await fetch("http://localhost:8000/teachers/unblock-schedule/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          teacher_id: blockTeacherId,
          day: block.day,
          start_time: block.start_time,
          end_time: block.end_time
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setBlockMsg("Bloqueo eliminado correctamente.");
      } else {
        setBlockMsg(data.detail || "Error al desbloquear horario.");
      }
    } catch {
      setBlockMsg("No se pudo conectar con el servidor.");
    }
  };

  // Validar horario de profesor
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

  function renderTab() {
    switch (activeTab) {
      case "teachers":
        // ...igual que antes...
        return (
          <section>
            <h3>Registrar Profesor</h3>
            <form onSubmit={handleAddTeacher} style={{ marginBottom: 10 }}>
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
            {addTeacherMsg && <div className="msg">{addTeacherMsg}</div>}
            {teachers.length > 0 && (
              <div>
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
          </section>
        );
      case "classrooms":
        // ...igual que antes...
        return (
          <section>
            <h3>Registrar Aula</h3>
            <form onSubmit={handleAddClassroom} style={{ marginBottom: 10 }}>
              <input
                type="text"
                placeholder="Nombre del aula"
                value={newClassroom.Name_Classroom}
                onChange={e => setNewClassroom({ ...newClassroom, Name_Classroom: e.target.value })}
                style={{ padding: 8, marginRight: 8 }}
                required
              />
              <input
                type="text"
                placeholder="Código del aula"
                value={newClassroom.Code_Classroom}
                onChange={e => setNewClassroom({ ...newClassroom, Code_Classroom: e.target.value })}
                style={{ padding: 8, marginRight: 8 }}
                required
              />
              <label style={{ marginRight: 8 }}>
                ¿Sala de sistemas?
                <input
                  type="checkbox"
                  checked={newClassroom.System_room}
                  onChange={e => setNewClassroom({ ...newClassroom, System_room: e.target.checked })}
                  style={{ marginLeft: 4 }}
                />
              </label>
              <button type="submit" style={{ padding: 8 }}>Agregar Aula</button>
            </form>
            {addClassroomMsg && <div className="msg">{addClassroomMsg}</div>}
            {classrooms.length > 0 && (
              <div>
                <strong>Aulas registradas:</strong>
                <ul>
                  {classrooms.map(c => (
                    <li key={c.Classroom_ID}>
                      {c.Name_Classroom} (Código: {c.Code_Classroom}, ID: {c.Classroom_ID}, Sistema: {c.System_room ? "Sí" : "No"})
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        );
      case "courses":
        // ...igual que antes...
        return (
          <section>
            <h3>Registrar Materia</h3>
            {teachers.length === 0 || classrooms.length === 0 ? (
              <div className="msg-warn">
                Primero debes registrar al menos un profesor y un aula.
              </div>
            ) : (
              <form onSubmit={handleAddCourse} style={{ marginBottom: 10 }}>
                <input
                  type="number"
                  placeholder="Código espacio académico"
                  value={newCourse.code_academic_space}
                  onChange={(e) => setNewCourse({ ...newCourse, code_academic_space: e.target.value })}
                  required
                />
                <input
                  type="text"
                  placeholder="Nombre espacio académico"
                  value={newCourse.name}
                  onChange={e => setNewCourse({ ...newCourse, name: e.target.value })}
                  style={{ padding: 8, marginRight: 8, width: 180 }}
                  required
                />
                <input
                  type="text"
                  placeholder="Franja"
                  value={newCourse.franja}
                  onChange={e => setNewCourse({ ...newCourse, franja: e.target.value })}
                  style={{ padding: 8, marginRight: 8, width: 100 }}
                  required
                />
                <input
                  type="text"
                  placeholder="Grupo"
                  value={newCourse.grupo}
                  onChange={e => setNewCourse({ ...newCourse, grupo: e.target.value })}
                  style={{ padding: 8, marginRight: 8, width: 80 }}
                  required
                />
                <input
                  type="number"
                  placeholder="Horas semanales"
                  value={newCourse.weekly_hours}
                  onChange={e => setNewCourse({ ...newCourse, weekly_hours: e.target.value })}
                  style={{ padding: 8, marginRight: 8, width: 120 }}
                  required
                />
                <select
                  value={newCourse.Teacher_ID}
                  onChange={e => setNewCourse({ ...newCourse, Teacher_ID: e.target.value })}
                  style={{ padding: 8, marginRight: 8, width: 150 }}
                  required
                >
                  <option value="">Selecciona un profesor</option>
                  {teachers.map(t => (
                    <option key={t.Teacher_ID} value={t.Teacher_ID}>
                      {t.Name} (ID: {t.Teacher_ID})
                    </option>
                  ))}
                </select>
                <select
                  value={newCourse.Classroom_ID}
                  onChange={e => setNewCourse({ ...newCourse, Classroom_ID: e.target.value })}
                  style={{ padding: 8, marginRight: 8, width: 180 }}
                  required
                >
                  <option value="">Selecciona un aula</option>
                  {classrooms.map(c => (
                    <option key={c.Classroom_ID} value={c.Classroom_ID}>
                      {c.Name_Classroom} (ID: {c.Classroom_ID})
                    </option>
                  ))}
                </select>
                <label style={{ marginRight: 8 }}>
                  ¿Materia requiere sala de sistemas?
                  <input
                    type="checkbox"
                    checked={newCourse.system_room}
                    onChange={e => setNewCourse({ ...newCourse, system_room: e.target.checked })}
                    style={{ marginLeft: 4 }}
                  />
                </label>
                <button type="submit" style={{ padding: 8 }}>Agregar Materia</button>
              </form>
            )}
            {addCourseMsg && <div className="msg">{addCourseMsg}</div>}
            {courses.length > 0 && (
              <div>
                <strong>Materias registradas:</strong>
                <ul>
                  {courses.map(c => (
                    <li key={c.Course_ID || c.course_ID}>
                      {c.code_academic_space} - {c.name} | Franja: {c.franja} | Grupo: {c.grupo} | Profesor ID: {c.Teacher_ID}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        );
      case "assign":
        const selectedCourse = courses.find(c => c.course_ID === Number(assignCourseId));
        const isThreeHourCourse = selectedCourse && Number(selectedCourse.weekly_hours) === 3;
        const blocksToShow = isThreeHourCourse
          ? ["7am-10am", "2pm-5pm", "6pm-9pm"]
          : [
              "7am-9am", "9am-11am", "11am-1pm",
              "2pm-4pm", "4pm-6pm", "6pm-8pm", "8pm-10pm"
            ];
        return (
          <section>
            <h3>Asignar Horario a Materia</h3>
            <form onSubmit={handleAssignSchedule} style={{ marginBottom: 10 }}>
              <select
                value={assignCourseId}
                onChange={e => setAssignCourseId(e.target.value)}
                required
              >
                <option value="">Selecciona una materia</option>
                {courses.map(c => (
                  <option key={c.course_ID} value={c.course_ID}>
                    {c.name} (ID: {c.course_ID})
                  </option>
                ))}
              </select>
              <select
                value={assignDay}
                onChange={e => setAssignDay(e.target.value)}
                required
              >
                <option value="">Día</option>
                <option>Lunes</option>
                <option>Martes</option>
                <option>Miércoles</option>
                <option>Jueves</option>
                <option>Viernes</option>
              </select>
              <select
                value={assignBlock}
                onChange={e => setAssignBlock(e.target.value)}
                required
              >
                <option value="">Bloque horario</option>
                {blocksToShow.map(block => (
                  <option key={block} value={block}>{block}</option>
                ))}
              </select>
              <button type="submit" style={{ padding: 8 }}>Asignar Horario</button>
            </form>
            {assignMsg && <div className="msg">{assignMsg}</div>}
          </section>
        );
      case "block":
        const blockDays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];
        const blockBlocks = [
          "7am-9am", "9am-11am", "11am-1pm",
          "2pm-4pm", "4pm-6pm", "6pm-8pm", "8pm-10pm",
          "7am-10am", "2pm-5pm", "6pm-9pm"
        ];
        return (
          <section>
            <h3>Bloquear Horario a Profesor</h3>
            <form onSubmit={handleBlockSchedule} style={{ marginBottom: 10 }}>
              <select
                value={blockTeacherId}
                onChange={e => setBlockTeacherId(e.target.value)}
                required
              >
                <option value="">Selecciona un profesor</option>
                {teachers.map(t => (
                  <option key={t.Teacher_ID} value={t.Teacher_ID}>
                    {t.Name} (ID: {t.Teacher_ID})
                  </option>
                ))}
              </select>
              <select
                value={blockDay}
                onChange={e => setBlockDay(e.target.value)}
                required
              >
                <option value="">Día</option>
                {blockDays.map(day => (
                  <option key={day} value={day}>{day}</option>
                ))}
              </select>
              <select
                value={blockBlock}
                onChange={e => setBlockBlock(e.target.value)}
                required
              >
                <option value="">Bloque horario</option>
                {blockBlocks.map(block => (
                  <option key={block} value={block}>{block}</option>
                ))}
              </select>
              <button type="submit" style={{ padding: 8 }}>Bloquear</button>
            </form>
            {blockMsg && <div className="msg">{blockMsg}</div>}

            {blockTeacherId && (
              <div style={{ marginTop: 24 }}>
                <h4>Horarios bloqueados</h4>
                {loadingBlocks ? (
                  <div>Cargando...</div>
                ) : currentBlocks.length === 0 ? (
                  <div style={{ color: "#aaa" }}>No hay horarios bloqueados para este profesor.</div>
                ) : (
                  <table className="calendar-table">
                    <thead>
                      <tr>
                        <th>Día</th>
                        <th>Inicio</th>
                        <th>Fin</th>
                        <th>Acción</th>
                      </tr>
                    </thead>
                    <tbody>
                      {currentBlocks.map((block, idx) => (
                        <tr key={idx}>
                          <td>{block.day}</td>
                          <td>{block.start_time}</td>
                          <td>{block.end_time}</td>
                          <td>
                            <button
                              style={{
                                background: "#ff5e5e",
                                color: "#fff",
                                border: "none",
                                borderRadius: 7,
                                padding: "6px 14px",
                                cursor: "pointer"
                              }}
                              onClick={() => handleUnblock(block)}
                            >
                              Desbloquear
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            )}
          </section>
        );
      case "validate":
        const days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];
        const blocks = [
          "7am-9am", "9am-11am", "11am-1pm",
          "2pm-4pm", "4pm-6pm", "6pm-8pm", "8pm-10pm",
          "7am-10am", "2pm-5pm", "6pm-9pm"
        ];
        let asignaciones = [];
        if (result && result.schedule) {
          asignaciones = result.schedule;
        }
        return (
          <section>
            <h3>Validar Horario de Profesor</h3>
            <form onSubmit={handleSubmit} style={{ marginBottom: 10 }}>
              <select
                value={teacherId}
                onChange={e => setTeacherId(e.target.value)}
                style={{ padding: 8, marginRight: 8, width: 200 }}
                required
              >
                <option value="">Selecciona un profesor</option>
                {teachers.map(t => (
                  <option key={t.Teacher_ID} value={t.Teacher_ID}>
                    {t.Name} (ID: {t.Teacher_ID})
                  </option>
                ))}
              </select>
              <button type="submit" style={{ padding: 8 }}>Validar Conflictos</button>
            </form>
            {error && <div className="msg-error">{error}</div>}
            <div style={{ overflowX: "auto", marginBottom: 24 }}>
              <table className="calendar-table">
                <thead>
                  <tr>
                    <th>Bloque</th>
                    {days.map(day => (
                      <th key={day}>{day}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {blocks.map(block => (
                    <tr key={block}>
                      <td><strong>{block}</strong></td>
                      {days.map(day => {
                        const asignacion = asignaciones.find(a => a.day === day && a.block === block);
                        return (
                          <td
                            key={day}
                            style={{
                              background: asignacion?.conflicto ? "#ff5e5e" : "#23283a",
                              color: asignacion?.conflicto ? "#fff" : "#e6e6e6",
                              fontWeight: asignacion?.conflicto ? "bold" : "normal",
                              border: asignacion?.conflicto ? "2px solid #ff5e5e" : "1px solid #2d3346"
                            }}
                            title={asignacion?.conflicto || ""}
                          >
                            {asignacion ? (
                              <>
                                {asignacion.materia}
                                <br />
                                <span style={{ fontSize: "0.9em", color: "#4e8cff" }}>
                                  {asignacion.salon}
                                </span>
                              </>
                            ) : ""}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {result && (
              <div className="result-box">
                <strong>{result.message}</strong>
                {result.conflicts && result.conflicts.length > 0 && (
                  <ul style={{ textAlign: "left" }}>
                    {result.conflicts.map((conflict, idx) => (
                      <li key={idx} style={{ color: "#ff5e5e" }}>{conflict}</li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </section>
        );
      case "calendar":
        // MATRIZ visual de todos los horarios
        const daysCal = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];
        const blocksCal = [
          "7am-9am", "9am-11am", "11am-1pm",
          "2pm-4pm", "4pm-6pm", "6pm-8pm", "8pm-10pm",
          "7am-10am", "2pm-5pm", "6pm-9pm"
        ];
        // Agrupa los horarios por bloque y día
        const grouped = {};
        allSchedules.forEach(s => {
          if (!grouped[s.block]) grouped[s.block] = {};
          if (!grouped[s.block][s.day]) grouped[s.block][s.day] = [];
          grouped[s.block][s.day].push(s);
        });
        return (
          <section>
            <h3>Calendario de todos los horarios</h3>
            <div style={{ overflowX: "auto", marginBottom: 24 }}>
              <table className="calendar-table">
                <thead>
                  <tr>
                    <th>Bloque</th>
                    {daysCal.map(day => (
                      <th key={day}>{day}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {blocksCal.map(block => (
                    <tr key={block}>
                      <td><strong>{block}</strong></td>
                      {daysCal.map(day => (
                        <td key={day}>
                          {(grouped[block] && grouped[block][day]) ? (
                            grouped[block][day].map((s, idx) => (
                              <div key={idx} style={{ marginBottom: 6 }}>
                                <span style={{ color: "#4e8cff", fontWeight: 600 }}>{s.materia}</span>
                                <br />
                                <span style={{ fontSize: "0.92em" }}>{s.profesor}</span>
                                <br />
                                <span style={{ fontSize: "0.92em", color: "#ffb84e" }}>{s.aula}</span>
                              </div>
                            ))
                          ) : ""}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="msg-warn" style={{ fontSize: "0.95em" }}>
              Si hay varias materias en un mismo bloque y día, se mostrarán todas en la celda.
            </div>
          </section>
        );
      case "graph":
        // Grafo global de conflictos
        if (!allSchedules || allSchedules.length === 0) {
          return (
            <section>
              <h3>Grafo de Conflictos</h3>
              <div className="msg-warn">No hay horarios registrados.</div>
            </section>
          );
        }

        // 1. Generar nodos en círculo
        const radius = 180;
        const centerX = 300;
        const centerY = 200;
        const n = allSchedules.length;
        const nodeIds = allSchedules.map(
          (a, idx) => `${a.materia}-${a.day}-${a.block}`
        );

        const graphNodes = allSchedules.map((a, idx) => {
          const angle = (2 * Math.PI * idx) / n;
          return {
            id: nodeIds[idx],
            data: { label: `${a.materia}\n${a.day} ${a.block}` },
            position: {
              x: centerX + radius * Math.cos(angle),
              y: centerY + radius * Math.sin(angle)
            },
            style: {
              border: a.conflicto ? "2px solid #ff5e5e" : "2px solid #4e8cff",
              background: a.conflicto ? "#ffb3b3" : "#e6e6fa",
              color: "#23283a",
              borderRadius: "50%",
              width: 90,
              height: 90,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              whiteSpace: "pre-line"
            },
            type: "default"
          };
        });

        // 2. Generar edges de conflicto
        let graphEdges = [];
        for (let i = 0; i < allSchedules.length; i++) {
          for (let j = i + 1; j < allSchedules.length; j++) {
            const a = allSchedules[i];
            const b = allSchedules[j];
            // Conflicto de aula
            if (
              a.day === b.day &&
              a.block === b.block &&
              a.aula === b.aula &&
              a.materia !== b.materia
            ) {
              graphEdges.push({
                id: `aula-${i}-${j}`,
                source: nodeIds[i],
                target: nodeIds[j],
                label: "Aula",
                animated: true,
                style: { stroke: "#ff5e5e", strokeWidth: 2 }
              });
            }
            // Conflicto de profesor
            if (
              a.day === b.day &&
              a.block === b.block &&
              a.profesor === b.profesor &&
              a.materia !== b.materia
            ) {
              graphEdges.push({
                id: `prof-${i}-${j}`,
                source: nodeIds[i],
                target: nodeIds[j],
                label: "Profesor",
                animated: true,
                style: { stroke: "#ffb84e", strokeWidth: 2 }
              });
            }
          }
        }

        return (
          <section>
            <h3>Grafo de Conflictos</h3>
            <div style={{ height: 440, background: "#23283a", borderRadius: 10, marginBottom: 16 }}>
              <ReactFlow
                nodes={graphNodes}
                edges={graphEdges}
                nodesDraggable={false}
                nodesConnectable={false}
                zoomOnScroll={false}
                panOnScroll
                style={{ background: "#23283a" }}
                fitView
              >
                <Background />
                <Controls />
              </ReactFlow>
            </div>
            <div className="msg-warn" style={{ fontSize: "0.95em" }}>
              <span style={{ color: "#ff5e5e" }}>Rojo</span>: conflicto de aula.{" "}
              <span style={{ color: "#ffb84e" }}>Naranja</span>: conflicto de profesor.<br />
              El grafo muestra todos los conflictos actuales del sistema.
            </div>
          </section>
        );
      default:
        return null;
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h2>Gestión de Horarios</h2>
        <nav className="tab-bar">
          {TABS.map(tab => (
            <button
              key={tab.key}
              className={activeTab === tab.key ? "tab active" : "tab"}
              onClick={() => setActiveTab(tab.key)}
            >
              {tab.label}
            </button>
          ))}
        </nav>
        <div className="tab-content">
          {renderTab()}
        </div>
      </header>
    </div>
  );
}

export default App;