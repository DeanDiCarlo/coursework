	public class Album {
		public String artist;
		public String producer;
		public String name;
		public Album(String artist, String producer, String name) {
			this.artist = artist;
			this.producer = producer;
			this.name = name;
		}
		@Override
		public String toString() {
			return String.format("[%s %s %s]", artist, producer, name);
		}
	}
