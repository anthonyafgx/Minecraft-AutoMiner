from Driver import Driver

def main():
    driver = Driver()

    if driver.Initialize():
        driver.RunLoop()

    driver.Shutdown()

if __name__ == "__main__":
    main()