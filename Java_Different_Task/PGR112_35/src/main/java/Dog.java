public class Dog extends Animal {
    private String breed;
    private boolean readyForAdoption;
    private int dailyFoodAmount;
    private String foodType;


    public Dog(int animalId, String name, int age, boolean vaccinated, int shelterId,
               String breed, boolean readyForAdoption, String foodType, int dailyFoodAmount) {
        super(animalId, name, age, vaccinated, shelterId);
        this.breed = breed;
        this.readyForAdoption = readyForAdoption;
        this.foodType = foodType;
        this.dailyFoodAmount = dailyFoodAmount;
    }

    public String getBreed() {
        return breed;
    }


    public boolean isReadyForAdoption() {
        return readyForAdoption;
    }

  public String getFoodType() {
        return foodType;
    }

  public int getDailyFoodAmount() {
        return dailyFoodAmount;
    }

    public void setDailyFoodAmount(int dailyFoodAmount) {
        this.dailyFoodAmount = dailyFoodAmount;
    }

    public void setBreed(String breed) {
        this.breed = breed;
    }

    public void setReadyForAdoption(boolean readyForAdoption) {
        this.readyForAdoption = readyForAdoption;
    }

    public void setFoodType(String foodType) {
        this.foodType = foodType;
    }
}
