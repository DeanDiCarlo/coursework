import java.lang.reflect.Field;

public class Search {
	// This provides a simple example of some reflection. You will need to
	// change this.
	public static boolean SearchStructure(Object obj, String searchString) {
		if (obj == null || searchString == null) {
			return false;
		}
		Class<?> klass = obj.getClass();
		Field [] fields = klass.getFields();
		for (Field f : fields) {
			try {
				Object value = f.get(obj);
				if (value instanceof String && ((String)value).contains(searchString)) {
					return true;
				}
			}
			catch (Exception e) {
				e.printStackTrace();
				System.exit(0);
			}
		}
		return false;
	}
	public static void main(String [] args) {
		Student student1 = new Student("John", "Doe", 3.1);
		Student student2 = new Student("Suzie", "Smith", 3.9);
		Album album1 = new Album("Beatles", "Meet the Beetles", "George Martin");
		
		System.out.println(SearchStructure(student1, "John"));   // true
		System.out.println(SearchStructure(student1, "Juan"));   // false
		System.out.println(SearchStructure(student2, "Juan"));   // false
		System.out.println(SearchStructure(student2, "Suz"));    // true
		
		System.out.println(SearchStructure(album1, "Martin"));   // true
		
		// For 565 students only:
		GradStudentClass gs = new GradStudentClass(student1, album1);
		System.out.println(SearchStructure(gs, "Martin"));		// true
		System.out.println(SearchStructure(gs, "Doe"));			// true
		System.out.println(SearchStructure(gs, "The Who"));		// false
	}
}
