#Lucas de Melo Lima Oliveira (lmlo)
#João Antonio de Lima Reis (jalr)


import random 





def fitness(n, k = 30):

    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    # If number is even, it's a composite number

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return 0
    return 1000



# Inicializa a população de inteiros
def init_population(size, min_val, max_val):
    pop = []
    for _ in range(size):
        num = (random.randint(min_val, max_val)+1)
        if num % 2 == 0:
            pop.append(num + 1)
        else:
            pop.append(num)
    return pop # população sempre impar, diminuindo o espaço de busca pela metade

# Seleção: Torneio binário
def selection(population, fitnesses):
    selected = []
    for _ in range(len(population)):
        if len(population) < 2:
            return population  # evita erro se houver apenas 1 indivíduo
        i, j = random.sample(range(len(population)), 2)
        selected.append(population[i] if fitnesses[i] > fitnesses[j] else population[j])
    return selected

# Crossover: combinação de bits
def crossover(parent1, parent2):
    p1 = format(parent1, 'b')
    p2 = format(parent2, 'b')
    max_len = max(len(p1), len(p2))
    p1 = p1.zfill(max_len)
    p2 = p2.zfill(max_len)
    point = random.randint(1, max_len - 1)
    child_bin = p1[:point] + p2[point:]
    return int(child_bin, 2)

# Mutação: troca aleatória de bits
def mutate(n, mutation_rate=0.05): # Mutação do ultimo bit sempre para 1, evitando numeros pares e exploração para luages indesejados no espaço de busca
    bits = list(format(n, 'b'))
    for i in range(len(bits)):
        if random.random() < mutation_rate:
            if i != len(bits) - 1:
                bits[i] = '1' if bits[i] == '0' else '0'
            else:
                bits[i] = '1'
    return int(''.join(bits), 2)

# Algoritmo evolutivo
def evolutionary_prime_search(pop_size=4, min_val=10**1000, max_val=10**1001, generations=1000):
    population = init_population(pop_size, min_val, max_val)

    for gen in range(generations):
        fitnesses = [fitness(ind) for ind in population]

        # Melhor indivíduo da geração
        best_idx = fitnesses.index(max(fitnesses))
        best_ind = population[best_idx]
        best_fit = fitnesses[best_idx]
        
        print(f"Geração {gen}: Melhor fitness = {best_fit:.5f}, Melhor indivíduo = {best_ind}")
        
        # Verifica se encontrou um primo
        if best_fit == 1000:
            print(f"\n✅ Primo encontrado na geração {gen}: {best_ind}")
            return best_ind
        
        # Seleção
        selected = selection(population, fitnesses)
        
        # Crossover com reposição até manter o tamanho original
        next_population = []
        while len(next_population) < pop_size:
            p1, p2 = random.sample(selected, 2)
            child = crossover(p1, p2)
            next_population.append(child)
        
        # Mutação
        population = [mutate(ind) for ind in next_population]
        
    print("\n❌ Nenhum primo encontrado após todas as gerações.")
    return None

# Executa o algoritmo
evolutionary_prime_search()