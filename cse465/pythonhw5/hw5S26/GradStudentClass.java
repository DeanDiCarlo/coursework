public class GradStudentClass {
	public Student student;
	public Album album;
	public GradStudentClass(Student student, Album album) {
		this.student = student;
		this.album = album;
	}
	@Override
	public String toString() {
		String studentStr = student == null ? null : student.toString();
		String albumStr = album == null ? null : album.toString();
		return String.format("[%s %s]", studentStr, albumStr);
	}
}
