public class Cat extends Animal {
    private String breed;
    private boolean neutered;
    private int dailyLitterAmount;
    private String lType;

    public Cat(int animalId, String name, int age, boolean vaccinated, int shelterId,
               String breed, boolean neutered, String lType, int dailyLitterAmount) {
        super(animalId, name, age, vaccinated, shelterId);
        this.breed = breed;
        this.neutered = neutered;
        this.lType = lType;
        this.dailyLitterAmount = dailyLitterAmount;
    }

    public String getBreed() {
        return breed;
    }

    public void setBreed(String breed) {
        this.breed = breed;
    }

    public boolean isNeutered() {
        return neutered;
    }

    public void setNeutered(boolean neutered) {
        this.neutered = neutered;
    }

    public String getlType() {
        return lType;
    }

    public void setlType(String lType) {
        this.lType = lType;
    }

    public int getDailyLitterAmount() {
        return dailyLitterAmount;
    }

    public void setDailyLitterAmount(int dailyLitterAmount) {
        this.dailyLitterAmount = dailyLitterAmount;
    }
}
