public class Bird extends Animal {
    private String species;
    private String cageSize;
    private boolean canFly;


    public Bird(int animalId, String name, int age, boolean vaccinated, int shelterId,
                String species, boolean canFly, String cageSize) {
        super(animalId, name, age, vaccinated, shelterId);
        this.species = species;
        this.canFly = canFly;
        this.cageSize = cageSize;
    }

    public String getSpecies() {
        return species;
    }

    public boolean isCanFly() {
        return canFly;
    }

    public String getCageSize() {
        return cageSize;
    }

}
