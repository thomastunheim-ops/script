public abstract class Animal {
    protected int id;
    protected String animalName;
    protected int age;
    protected boolean vaccinated;
    protected int shelterId;

    public Animal(int id, String animalName, int age, boolean vaccinated, int shelterId) {
        this.id = id;
        this.animalName = animalName;
        this.age = age;
        this.vaccinated = vaccinated;
        this.shelterId = shelterId;
    }

    public int getId() {
        return id;
    }

    public String getAnimalName() {
        return animalName;
    }

    public int getAge() {
        return age;
    }

    public boolean isVaccinated() {
        return vaccinated;
    }

    public int getShelterId() {
        return shelterId;
    }
}
