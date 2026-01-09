import random
import datetime

def generate_account_number():
    """Generate a unique 12-digit account number with prefix and checksum."""
    prefix = "10"  # can represent your bank or country code
    timestamp = datetime.datetime.now().strftime("%y%m%d")  # YYMMDD
    random_part = str(random.randint(1000, 9999))
    account_number = prefix + timestamp[-4:] + random_part
    return account_number


def generate_routing_number():
    # Generate first 8 random digits
    digits = [random.randint(0, 9) for _ in range(8)]
    
    # Calculate checksum (using ABA formula)
    checksum = (7*(digits[0] + digits[3] + digits[6]) +
                3*(digits[1] + digits[4] + digits[7]) +
                9*(digits[2] + digits[5])) % 10
    check_digit = (10 - checksum) % 10
    
    digits.append(check_digit)
    return ''.join(map(str, digits))

def generate_card_number():
    # Generate first 8 random digits
    digits = [random.randint(0, 17) for _ in range(8)]
    
    # Calculate checksum (using ABA formula)
    checksum = (7*(digits[0] + digits[3] + digits[6]) +
                3*(digits[1] + digits[4] + digits[7]) +
                9*(digits[2] + digits[5])) % 10
    check_digit = (10 - checksum) % 10
    
    digits.append(check_digit)
    return ''.join(map(str, digits))

def generate_cvv():
    # Generate first 8 random digits
    digits = [random.randint(0, 9) for _ in range(2)]
    # Calculate checksum (using ABA formula)
    checksum = (7*(digits[0] ) + 3*(digits[1] + digits[0] ) + 9*(digits[0] + digits[1])) % 10
    check_digit = (10 - checksum) % 10
    
    digits.append(check_digit)
    return ''.join(map(str, digits))


