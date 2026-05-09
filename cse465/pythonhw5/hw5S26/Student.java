public class Student {
	public String firstName;
	public String lastName;
	public double GPA;
	public Student(String firstName, String lastName, double GPA) {
		this.firstName = firstName;
		this.lastName = lastName;
		this.GPA = GPA;
	}
	@Override
	public String toString() {
		return String.format("[%s %s %f]", firstName, lastName, GPA);
	}
}
