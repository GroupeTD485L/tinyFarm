package com.example.tinyfarm.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.Duration;

import com.example.tinyfarm.entity.Produit;
import com.example.tinyfarm.entity.Commerce;
import com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.repository.CommerceRepository;

import java.util.Optional;

@Service
public class CommerceService {
    private final CommerceRepository commerceRepository;

    public CommerceService(CommerceRepository commerceRepository) {
        this.commerceRepository = commerceRepository;
    }

    @Transactional
    public Commerce addCommerce(Commerce commerce) {
        return commerceRepository.save(commerce);
    }

    @Transactional
    public void deleteCommerce(Long id) {
        commerceRepository.deleteById(id);
    }

    @Transactional
    public void executeTransaction(Long id, int quantite) {
        Optional<Commerce> existingCommerce = commerceRepository.findById(id);
        Commerce commerce = existingCommerce.get();
        Ferme vendeur = commerce.getVendeur();
        Ferme acheteur = commerce.getAcheteur();
        float prixMoyen = commerceRepository.findAveragePriceById(id);
        float montantTransaction = quantite*prixMoyen;
        List<Commerce> commerces = commerceRepository.findAllByProduitOrderByPrixAsc(ProduitRepository.findById(id));
        for (Commerce c : commerces) {
            if (c.getQuantite()<=quantite) {
                c.getVendeur().setEcus(c.getQuantite()*prixMoyen);
                quantite-=c.getQuantite();
                commerceRepository.deleteById(c.getIdTransac());
            } else if (c.getQuantite()>quantite) {
                c.setQuantite(c.getQuantite()-quantite);
                break;
            }
        }
        acheteur.setEcus(acheteur.getEcus()-montantTransaction);// On retire les écus à l'acheteur
        //TODO : Retirer les produits aux vendeurs et les donner à l'acheteur
        if (quantite == commerce.getQuantite()) {
            commerceRepository.deleteById(id);
        } 
    }

    @Transactional
    public void checkCommerce(Long id) {
        Optional<Commerce> existingCommerce = commerceRepository.findById(id);
        if (Duration.between(LocalDateTime.now(), existingCommerce.get().getDateAchat()).toDays() >= 7) { // Si la date actuelle dépasse la date d'achat (qui est la date de création du commerce) + 7 jours, alors on supprime le commerce
            commerceRepository.deleteById(id);
            // TODO : Remettre les produits du commerce dans la réserve
        }
    }

}