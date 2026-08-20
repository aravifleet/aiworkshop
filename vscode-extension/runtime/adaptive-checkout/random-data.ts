const FIRST_NAMES = ['Ava', 'Liam', 'Noah', 'Emma', 'Mia', 'Lucas', 'Ethan'];
const LAST_NAMES = ['Parker', 'Brooks', 'Reed', 'Hayes', 'Turner', 'Coleman', 'Bailey'];
const STREETS = ['742 Evergreen Terrace', '123 Maple Street', '88 Sunset Drive', '451 Oak Avenue'];
const CITIES = ['Austin', 'Denver', 'Seattle', 'Portland', 'Phoenix'];
const STATES = ['CA', 'CO', 'TX', 'WA', 'OR', 'AZ', 'NY'];

function pick<T>(values: T[]) {
  return values[Math.floor(Math.random() * values.length)];
}

function digits(length: number) {
  return Array.from({ length }, () => Math.floor(Math.random() * 10)).join('');
}

export function buildRandomUsAddress() {
  const firstName = pick(FIRST_NAMES);
  const lastName = pick(LAST_NAMES);
  const city = pick(CITIES);
  const state = pick(STATES);

  return {
    city,
    company: `QA ${pick(LAST_NAMES)} Labs`,
    email: `qa.${firstName.toLowerCase()}.${Date.now()}@example.com`,
    firstName,
    giftMessage: `Automated checkout ${Date.now()}`,
    houseAccountNumber: digits(8),
    lastName,
    phone: `555${digits(7)}`,
    postalCode: `${Math.floor(10000 + Math.random() * 89999)}`,
    state,
    street1: pick(STREETS),
    street2: `Suite ${Math.floor(100 + Math.random() * 900)}`,
  };
}
